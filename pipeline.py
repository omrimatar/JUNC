"""
pipeline.py — JUNC analysis pipeline orchestrator.

run_pipeline(xlsx_file, queue_params=None) accepts either a file path (str)
or a file-like object (e.g. a Streamlit UploadedFile) and returns five
values: four finished files as bytes objects ready for download, plus an
extra_data dict containing raw per-run data for Additional Analysis.
"""

import os
import shutil
import tempfile
import threading

import Phaser
from Main_Diagram import run_diagram_pipeline
from Main_Table import run_table_pipeline
from Main_ID import run_id_pipeline
from additional_analysis import make_queue_excel

_SRC_DIR = os.path.dirname(os.path.abspath(__file__))

# Prevent concurrent runs from corrupting each other when running locally.
# (A real multi-user deployment would use per-request isolated processes instead.)
_pipeline_lock = threading.Lock()


def run_pipeline(xlsx_file, queue_params=None):
    """
    Run the full JUNC traffic-junction analysis pipeline.

    Parameters
    ----------
    xlsx_file : str or file-like object
        Path to volume_calculator.xlsx, or any object with a .read() method.
    queue_params : dict, optional
        Parameters forwarded to queue_length().  Keys and defaults:
          discard_green_time=False, basic_lost_capacity=200,
          poisson=0.95, l=7, phf=0.9, cycle_time=120

    Returns
    -------
    tuple[bytes, bytes, bytes, bytes, dict]
        (diagram_pptx, table_pptx, id_pptx, queue_xlsx, extra_data)
        extra_data contains car_sum_am/pm, pulp_vars_am/pm, car_length_dict
        for use in the Additional Analysis section.
    """
    if queue_params is None:
        queue_params = {}

    with _pipeline_lock:
        workdir = tempfile.mkdtemp(prefix="junc_")
        orig_dir = os.getcwd()
        try:
            # --- Copy inputs into workdir ---
            xlsx_dst = os.path.join(workdir, "volume_calculator.xlsx")
            if hasattr(xlsx_file, "read"):
                data = xlsx_file.read()
                if hasattr(xlsx_file, "seek"):
                    xlsx_file.seek(0)
                with open(xlsx_dst, "wb") as f:
                    f.write(data)
            else:
                shutil.copy2(xlsx_file, xlsx_dst)

            # OUTPUT.xlsx is used by Phaser to write results; copy the blank template
            output_src = os.path.join(_SRC_DIR, "OUTPUT.xlsx")
            if os.path.exists(output_src):
                shutil.copy2(output_src, os.path.join(workdir, "OUTPUT.xlsx"))

            # --- Switch to workdir so all relative-path code works ---
            os.chdir(workdir)

            # --- Run the three pipeline stages ---
            phsr_list, excel_props, car_length_dict, phaser_extra = Phaser.main(
                queue_params=queue_params
            )

            junc_diagram, diagram_bytes = run_diagram_pipeline(phsr_list, excel_props)
            junc_table,   table_bytes   = run_table_pipeline(junc_diagram)
            id_bytes                    = run_id_pipeline(junc_table, junc_diagram)
            queue_bytes                 = make_queue_excel(car_length_dict, queue_params)

            extra_data = {**phaser_extra, "car_length_dict": car_length_dict}

            return diagram_bytes, table_bytes, id_bytes, queue_bytes, extra_data

        finally:
            os.chdir(orig_dir)
            shutil.rmtree(workdir, ignore_errors=True)
