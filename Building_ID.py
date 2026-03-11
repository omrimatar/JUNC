import os
from pptx import Presentation

# Absolute path to the project source directory — used for reading templates
_SRC_DIR = os.path.dirname(os.path.abspath(__file__))


def create_new_id_templates_file():
    """Creates a working copy of the ID template in the current directory."""
    src = os.path.join(_SRC_DIR, "ID_template", "id_template.pptx")
    prs_id = Presentation(src)
    prs_id.save("id_template.pptx")


def delete_temp_id_pres():
    """Deletes all temporary PPTX files created during ID generation."""
    prs_to_del = ["id_template.pptx", "id_info.pptx"]
    for temp_prs in prs_to_del:
        if os.path.exists(temp_prs):
            os.remove(temp_prs)
