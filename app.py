"""
app.py — JUNC Streamlit UI (full form + live junction schematic).

Run with:  streamlit run app.py
"""

from io import BytesIO
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from docs import (
    render_hcm_delay_docs, render_hcm_queue95_docs,
    render_junc_guide, render_queue_poisson_docs,
)
from additional_analysis import (
    compute_hcm_delay, compute_hcm_queue95,
    make_hcm_excel, make_queue_excel,
)
from pipeline import run_pipeline, PipelineError
from queue_length import queue_length as _queue_length
from ui_diagram import draw_junction
from ui_excel import (
    DIRECTIONS, MOVEMENTS, LANE_TYPES,
    create_excel_from_state, default_state, read_excel_to_state,
)

PPTX_MIME  = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
XLSX_MIME  = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
ZIP_MIME   = "application/zip"
_SRC_DIR   = Path(__file__).parent
_TEMPLATE  = _SRC_DIR / "volume_calculator.xlsx"


def _pptx_to_png_bytes(pptx_bytes: bytes) -> bytes | None:
    """Export slide 1 of a PPTX as PNG using PowerPoint COM (Windows only).
    Returns None silently if PowerPoint / comtypes is unavailable."""
    import os, shutil, tempfile
    try:
        import comtypes.client
    except ImportError:
        return None
    tmpdir = tempfile.mkdtemp(prefix="junc_png_")
    try:
        pptx_path = os.path.join(tmpdir, "slide.pptx")
        png_path  = os.path.join(tmpdir, "slide.png")
        with open(pptx_path, "wb") as fh:
            fh.write(pptx_bytes)
        ppt = comtypes.client.CreateObject("PowerPoint.Application")
        ppt.Visible = 1
        try:
            pres = ppt.Presentations.Open(pptx_path, WithWindow=False)
            pres.Slides[1].Export(png_path, "PNG", 1920, 1440)
            pres.Close()
        finally:
            ppt.Quit()
        if os.path.exists(png_path):
            with open(png_path, "rb") as fh:
                return fh.read()
    except Exception:
        return None
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
    return None


def _make_full_zip(diagram_b: bytes, table_b: bytes, id_b: bytes, queue_b: bytes) -> bytes:
    """Bundle all output files + PNG slide exports into a single ZIP."""
    import io, zipfile
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("Diagram.pptx",      diagram_b)
        zf.writestr("Table.pptx",        table_b)
        zf.writestr("ID.pptx",           id_b)
        zf.writestr("QueueLengths.xlsx", queue_b)
        for label, data in (("Diagram", diagram_b), ("Table", table_b)):
            png = _pptx_to_png_bytes(data)
            if png:
                zf.writestr(f"{label}.png", png)
    buf.seek(0)
    return buf.getvalue()

_QUEUE_NAMES = [
    "NR_length",  "NRT_length", "NT_length",  "NTL_length", "NL_length",  "NRTL_length", "NRL_length",
    "SR_length",  "SRT_length", "ST_length",  "STL_length", "SL_length",  "SRTL_length", "SRL_length",
    "ER_length",  "ERT_length", "ET_length",  "ETL_length", "EL_length",  "ERTL_length", "ERL_length",
    "WR_length",  "WRT_length", "WT_length",  "WTL_length", "WL_length",  "WRTL_length", "WRL_length",
]
_MOVE_EN = {
    "R": "Right", "RT": "Right + Through", "T": "Through",
    "TL": "Through + Left", "L": "Left",
    "RTL": "Right + Through + Left", "RL": "Right + Left",
}
_DIR_EN = {"N": "North", "S": "South", "E": "East", "W": "West"}

# Friendly labels for data-editor display (code → display label)
_MOVE_LABELS = {"R": "Right Turn", "T": "Through", "L": "Left Turn"}
_LANE_LABELS = {
    "R":   "R  – Right only",
    "RT":  "RT – Right + Through",
    "T":   "T  – Through only",
    "TL":  "TL – Through + Left",
    "L":   "L  – Left only",
    "RTL": "RTL – All shared",
    "RL":  "RL – Right + Left",
}
_DIR_LABELS = {"N": "North", "S": "South", "E": "East", "W": "West"}

# ---------------------------------------------------------------------------
# Page config & global CSS
# ---------------------------------------------------------------------------
st.set_page_config(page_title="JUNC", page_icon="🚦", layout="wide")

st.markdown("""
<style>
[data-testid="stTextInput"] input {
    direction: rtl;
    text-align: right;
}
[data-testid="stDataFrame"] td, [data-testid="stDataFrame"] th {
    padding: 3px 6px !important;
    font-size: 13px !important;
}
[data-testid="stNumberInput"] input {
    padding: 4px 8px !important;
}
section[data-testid="stSidebar"] h2 { margin-top: 0.4rem; }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Session-state initialisation
# ---------------------------------------------------------------------------
if "junc_state" not in st.session_state:
    st.session_state.junc_state = default_state()

if "results" not in st.session_state:
    st.session_state.results = None         # (diagram_bytes, table_bytes, id_bytes, queue_bytes)

if "extra_data" not in st.session_state:
    st.session_state.extra_data = None      # {car_sum_am/pm, pulp_vars_am/pm, car_length_dict}

if "queue_recalc" not in st.session_state:
    st.session_state.queue_recalc = None    # {car_length_dict, params} after manual recalculation

_DEFAULT_QUEUE_PARAMS = {
    "discard_green_time": False,
    "basic_lost_capacity": 200,
    "poisson": 0.95,
    "l": 7,
    "phf": 0.9,
    "cycle_time": 120,
}
if "queue_params" not in st.session_state:
    st.session_state.queue_params = dict(_DEFAULT_QUEUE_PARAMS)

_DEFAULT_HCM_GREEN_TIMES = {d: {"am": 40, "pm": 40} for d in ["N", "S", "E", "W"]}
if "hcm_green_times" not in st.session_state:
    st.session_state.hcm_green_times = {d: dict(v) for d, v in _DEFAULT_HCM_GREEN_TIMES.items()}

_DEFAULT_HCM_PARAMS = {
    "cycle_time": 120, "saturation_flow": 1800,
    "T": 0.25, "k": 0.5, "PF": 1.0, "I": 1.0, "l": 7,
}
if "hcm_params" not in st.session_state:
    st.session_state.hcm_params = dict(_DEFAULT_HCM_PARAMS)

if "hcm_delay_results" not in st.session_state:
    st.session_state.hcm_delay_results = None

if "hcm_queue95_results" not in st.session_state:
    st.session_state.hcm_queue95_results = None

if "editor_version" not in st.session_state:
    st.session_state.editor_version = 0

if "auto_run" not in st.session_state:
    st.session_state.auto_run = False

if "last_imported_file_id" not in st.session_state:
    st.session_state.last_imported_file_id = None

if "full_zip" not in st.session_state:
    st.session_state.full_zip = None

if "excel_template" not in st.session_state:
    if _TEMPLATE.exists():
        st.session_state.excel_template = _TEMPLATE.read_bytes()
    else:
        st.session_state.excel_template = None

state = st.session_state.junc_state
ver   = st.session_state.editor_version


# ---------------------------------------------------------------------------
# Helper: data-editor that writes back into *state* automatically
# ---------------------------------------------------------------------------

def _make_vol_df(period: str) -> pd.DataFrame:
    return pd.DataFrame(
        {d: {_MOVE_LABELS[m]: int(state["volumes"][period][d][m]) for m in MOVEMENTS}
         for d in DIRECTIONS},
    )

def _make_lane_df(key: str) -> pd.DataFrame:
    return pd.DataFrame(
        {d: {_LANE_LABELS[lt]: int(state[key][d][lt]) for lt in LANE_TYPES}
         for d in DIRECTIONS},
    )

def _int_col_cfg(label: str):
    return st.column_config.NumberColumn(label, min_value=0, step=1, format="%d")


# ---------------------------------------------------------------------------
# ── SIDEBAR ─────────────────────────────────────────────────────────────────
# ---------------------------------------------------------------------------
with st.sidebar:

    # ── Version badge ─────────────────────────────────────────────────────────
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            border: 1px solid #e94560;
            border-radius: 10px;
            padding: 10px 16px 8px 16px;
            margin-bottom: 18px;
            text-align: center;
        ">
            <span style="
                font-size: 11px;
                font-weight: 600;
                letter-spacing: 3px;
                color: #a0a8b8;
                text-transform: uppercase;
            ">JUNC Analyzer</span><br>
            <span style="
                font-size: 26px;
                font-weight: 800;
                letter-spacing: 1px;
                color: #e94560;
                line-height: 1.2;
            ">v 1.1</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Fonts ────────────────────────────────────────────────────────────────
    st.header("Fonts")
    st.caption(
        "These fonts must be installed on your PC to correctly view "
        "the downloaded PPTX files."
    )
    st.markdown(
        "**1. Traffic Arrows** (phase arrows)  \n"
        "[⬇ Download TrafficArrows.ttf]"
        "(https://github.com/omrimatar/JUNC/raw/master/fonts/TrafficArrows.ttf)"
    )
    st.markdown(
        "**2. Assistant** (Hebrew text)  \n"
        "[⬇ Download from Google Fonts](https://fonts.google.com/specimen/Assistant)"
    )
    st.caption("To install: double-click the .ttf file → click Install → restart PowerPoint.")

    try:
        from font_installer import get_status, install_fonts
        font_status = get_status()
        all_ok = all(font_status.values())

        if all_ok:
            st.success("✅ All fonts installed — PPTX files will display correctly on this PC.")
        else:
            missing = [n for n, ok in font_status.items() if not ok]
            st.warning(f"{len(missing)} font(s) missing on this PC")
            for name in missing:
                st.caption(f"• {name}")

        with st.expander("Font details"):
            for name, ok in font_status.items():
                st.caption(f"{'✅' if ok else '❌'} {name}")

        if not all_ok:
            if st.button("Install Missing Fonts", use_container_width=True):
                with st.spinner("Installing…"):
                    results = install_fonts(download_assistant=True)
                for name, ok, msg in results:
                    (st.success if ok else st.error)(f"{name}: {msg}")
                st.info("Restart PowerPoint if it was open.")
                st.rerun()
    except ImportError:
        pass   # cloud/Linux — download links above are sufficient
    except Exception as exc:
        st.caption(f"Font check error: {exc}")

    st.divider()

    # ── Project info ─────────────────────────────────────────────────────────
    st.header("Project")
    state["junc"]["more_info"] = st.text_input(
        "Project name", value=str(state["junc"].get("more_info") or ""),
        placeholder="שם הפרויקט",
    )
    state["junc"]["proj_counter"] = st.number_input(
        "Project #", value=int(state["junc"].get("proj_counter") or 0),
        min_value=0, step=1,
    )

    st.divider()

    # ── Download blank template ───────────────────────────────────────────────
    st.header("Template")
    if st.session_state.excel_template:
        st.download_button(
            "⬇ Download Blank Template",
            st.session_state.excel_template,
            "volume_calculator.xlsx",
            XLSX_MIME,
            use_container_width=True,
            help="Download the blank volume_calculator.xlsx with all instructions and formatting.",
        )
    else:
        st.caption("Template file not found.")

    st.divider()

    # ── Import from Excel ─────────────────────────────────────────────────────
    st.header("Import Excel")
    st.caption("Load an existing volume_calculator.xlsx to fill the form.")
    uploaded = st.file_uploader("Choose file", type=["xlsx"],
                                label_visibility="collapsed")
    if uploaded and uploaded.file_id != st.session_state.last_imported_file_id:
        try:
            new_state = read_excel_to_state(uploaded.read())
            st.session_state.junc_state = new_state
            state = new_state
            st.session_state.editor_version += 1
            st.session_state.last_imported_file_id = uploaded.file_id
            st.session_state.auto_run = True
            st.rerun()
        except Exception as exc:
            st.error(f"Import failed: {exc}")

    st.divider()

    # ── Run analysis ──────────────────────────────────────────────────────────
    st.header("Analysis")

    run_disabled = st.session_state.excel_template is None
    if run_disabled:
        st.warning("volume_calculator.xlsx template not found next to app.py.")

    run_clicked = st.button(
        "▶  Run Analysis",
        type="primary",
        use_container_width=True,
        disabled=run_disabled,
    )

    # Download buttons (shown after a successful run)
    if st.session_state.results:
        diagram_b, table_b, id_b, queue_b = st.session_state.results
        st.success("Results ready")
        st.download_button("⬇ Diagram",       diagram_b, "Diagram.pptx",      PPTX_MIME,
                           use_container_width=True)
        st.download_button("⬇ Table",         table_b,   "Table.pptx",        PPTX_MIME,
                           use_container_width=True)
        st.download_button("⬇ ID Sheet",      id_b,      "ID.pptx",           PPTX_MIME,
                           use_container_width=True)
        st.download_button("⬇ Queue Lengths", queue_b,   "QueueLengths.xlsx", XLSX_MIME,
                           use_container_width=True)
        st.divider()
        if st.session_state.full_zip is None:
            if st.button("📦 Prepare Full Analysis ZIP", use_container_width=True,
                         help="Exports Diagram + Table to PNG and bundles all files into a ZIP."):
                with st.spinner("Exporting slides to PNG…"):
                    st.session_state.full_zip = _make_full_zip(diagram_b, table_b, id_b, queue_b)
                st.rerun()
        else:
            st.download_button(
                "⬇ Full Analysis (ZIP)",
                st.session_state.full_zip,
                "JUNC_Full_Analysis.zip",
                ZIP_MIME,
                use_container_width=True,
            )
        _log = (st.session_state.extra_data or {}).get("log", "")
        if _log.strip():
            with st.expander("Analysis log"):
                st.code(_log, language="")


# ---------------------------------------------------------------------------
# ── MAIN AREA ───────────────────────────────────────────────────────────────
# ---------------------------------------------------------------------------
st.title("JUNC — Traffic Junction Optimizer")

with st.expander("ℹ  Info", expanded=False):
    _i1, _i2, _i3, _i4 = st.tabs([
        "🚦 Using JUNC",
        "📏 Queue Length (Poisson)",
        "⏱ HCM Delay & LOS",
        "📊 HCM 95th Queue",
    ])
    with _i1:
        render_junc_guide()
    with _i2:
        render_queue_poisson_docs()
    with _i3:
        render_hcm_delay_docs()
    with _i4:
        render_hcm_queue95_docs()

col_diagram, col_inputs = st.columns([4, 6], gap="large")

# ── Left column: live junction schematic ─────────────────────────────────────
with col_diagram:
    st.subheader("Junction Schematic")
    fig = draw_junction(state)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    with st.expander("Volume breakdown", expanded=False):
        rows = []
        for d in DIRECTIONS:
            for period, label in (("morning", "AM"), ("evening", "PM")):
                vols = state["volumes"][period][d]
                rows.append({
                    "Dir": d, "Period": label,
                    "R": vols["R"], "T": vols["T"], "L": vols["L"],
                    "Total": vols["R"] + vols["T"] + vols["L"],
                })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


# ── Right column: tabbed data-entry ──────────────────────────────────────────
with col_inputs:
    tab_vol, tab_lanes, tab_nataz, tab_settings = st.tabs(
        ["🚗 Volumes", "🛣 Lanes", "🚌 Nataz", "⚙ Settings"]
    )

    col_cfg = {d: _int_col_cfg(_DIR_LABELS[d]) for d in DIRECTIONS}

    # ── Volumes tab ───────────────────────────────────────────────────────────
    with tab_vol:
        st.markdown("**Morning (AM)** — vehicles per hour")
        am_df = _make_vol_df("morning")
        edited_am = st.data_editor(
            am_df, key=f"am_{ver}",
            column_config=col_cfg,
            use_container_width=True,
        )
        for d in DIRECTIONS:
            for m in MOVEMENTS:
                val = edited_am.at[_MOVE_LABELS[m], d]
                state["volumes"]["morning"][d][m] = 0 if pd.isna(val) else int(val)

        st.divider()

        st.markdown("**Evening (PM)** — vehicles per hour")
        pm_df = _make_vol_df("evening")
        edited_pm = st.data_editor(
            pm_df, key=f"pm_{ver}",
            column_config=col_cfg,
            use_container_width=True,
        )
        for d in DIRECTIONS:
            for m in MOVEMENTS:
                val = edited_pm.at[_MOVE_LABELS[m], d]
                state["volumes"]["evening"][d][m] = 0 if pd.isna(val) else int(val)

        st.caption("R = right turn · T = through · L = left turn")

    # ── Lanes tab ─────────────────────────────────────────────────────────────
    with tab_lanes:
        st.markdown(
            "**Lane configuration** — enter number of lanes per type. "
            "Shared lanes (e.g. RT = right + through) count once."
        )
        lane_df = _make_lane_df("lanes")
        edited_lanes = st.data_editor(
            lane_df, key=f"lanes_{ver}",
            column_config=col_cfg,
            use_container_width=True,
        )
        for d in DIRECTIONS:
            for lt in LANE_TYPES:
                val = edited_lanes.at[_LANE_LABELS[lt], d]
                state["lanes"][d][lt] = 0 if pd.isna(val) else int(val)

        st.caption(
            "R · RT · T · TL · L = dedicated lanes | "
            "RTL = shared right+through+left | RL = shared right+left"
        )

    # ── Nataz tab ─────────────────────────────────────────────────────────────
    with tab_nataz:
        st.markdown("**Nataz (נת״צ) — Public Transit Lane Designations**")
        st.caption(
            "Enter the number of dedicated bus lanes for each simple lane type (R / T / L). "
            "For complex lanes (RT, TL, RL, RTL), enter a code indicating which movement "
            "within that lane is designated for public transit:\n\n"
            "| Code | Movement |\n"
            "|------|----------|\n"
            "| `1`  | Entire lane (all movements) |\n"
            "| `2`  | Right only |\n"
            "| `3`  | Through only |\n"
            "| `4`  | Left only |\n"
            "| `5`  | Right + Through |\n"
            "| `6`  | Right + Left |\n"
            "| `7`  | Through + Left |\n\n"
            "Nataz designations are shown in the output PowerPoint. "
            "Bus-only movements are also excluded from private-car routing."
        )
        nataz_df = _make_lane_df("nataz")
        edited_nataz = st.data_editor(
            nataz_df, key=f"nataz_{ver}",
            column_config=col_cfg,
            use_container_width=True,
        )
        for d in DIRECTIONS:
            for lt in LANE_TYPES:
                val = edited_nataz.at[_LANE_LABELS[lt], d]
                state["nataz"][d][lt] = 0 if pd.isna(val) else int(val)

    # ── Settings tab ─────────────────────────────────────────────────────────
    with tab_settings:
        s_left, s_right = st.columns(2)

        with s_left:
            st.markdown("**Junction settings**")
            state["instructions"]["capacity"] = st.number_input(
                "Capacity (veh/h/lane)", min_value=1,
                value=int(state["instructions"].get("capacity") or 1800),
                step=100, key=f"cfg_cap_{ver}",
            )
            state["instructions"]["inflation"] = st.number_input(
                "MCU inflation factor",
                value=float(state["instructions"].get("inflation") or 1.0),
                step=0.05, format="%.2f", key=f"cfg_inf_{ver}",
            )
            state["instructions"]["geo_ns"] = st.number_input(
                "Geometry N-S (lanes)", min_value=1,
                value=int(state["instructions"].get("geo_ns") or 3),
                step=1, key=f"cfg_gns_{ver}",
            )
            state["instructions"]["geo_ew"] = st.number_input(
                "Geometry E-W (lanes)", min_value=1,
                value=int(state["instructions"].get("geo_ew") or 3),
                step=1, key=f"cfg_gew_{ver}",
            )

            st.divider()
            st.markdown("**Phase permissions**")
            state["instructions"]["nlsl"] = int(
                st.checkbox("Allow NL + SL simultaneous",
                            value=bool(state["instructions"].get("nlsl")),
                            key=f"chk_nlsl_{ver}")
            )
            state["instructions"]["elwl"] = int(
                st.checkbox("Allow EL + WL simultaneous",
                            value=bool(state["instructions"].get("elwl")),
                            key=f"chk_elwl_{ver}")
            )
            state["instructions"]["img5"] = int(
                st.checkbox("Enable 5th image",
                            value=bool(state["instructions"].get("img5")),
                            key=f"chk_img5_{ver}")
            )
            state["instructions"]["img6"] = int(
                st.checkbox("Enable 6th image",
                            value=bool(state["instructions"].get("img6")),
                            key=f"chk_img6_{ver}")
            )

        with s_right:
            st.markdown("**LRT settings**")
            lrt_on = st.checkbox(
                "LRT present at junction",
                value=bool(state["rakal"].get("lrt_enabled")),
                key=f"chk_lrt_{ver}",
            )
            state["rakal"]["lrt_enabled"] = int(lrt_on)

            if lrt_on:
                state["junc"]["lrt_line_name"] = st.text_input(
                    "LRT line name",
                    value=str(state["junc"].get("lrt_line_name") or ""),
                    placeholder="שם הקו",
                    key=f"lrt_name_{ver}",
                )
                state["rakal"]["cycle_time"] = st.number_input(
                    "Signal cycle time (s)", min_value=1,
                    value=int(state["rakal"].get("cycle_time") or 120),
                    step=5, key=f"lrt_cycle_{ver}",
                )
                state["rakal"]["lost_time"] = st.number_input(
                    "Lost time per phase (s)", min_value=0,
                    value=int(state["rakal"].get("lost_time") or 3),
                    step=1, key=f"lrt_lost_{ver}",
                )
                state["rakal"]["gen_lost_time"] = st.number_input(
                    "Total lost time (s)", min_value=0,
                    value=int(state["rakal"].get("gen_lost_time") or 6),
                    step=1, key=f"lrt_glost_{ver}",
                )
                state["rakal"]["headway"] = st.number_input(
                    "LRT headway (s)", min_value=1,
                    value=int(state["rakal"].get("headway") or 3),
                    step=1, key=f"lrt_hw_{ver}",
                )
                state["rakal"]["mcu"] = st.number_input(
                    "MCU", min_value=0.1,
                    value=float(state["rakal"].get("mcu") or 1.0),
                    step=0.125, format="%.3f", key=f"lrt_mcu_{ver}",
                )
                # LRT direction — matches c_optimization encoding:
                # instructions[8]: 0=none, 1=N-S, 2=N-S+E side, 3=N-S+W side, 4/5/6/7=corner (paired)
                # instructions[9]: 0=none, 1=E-W, 2=E-W+N side, 3=E-W+S side, 4/5/6/7=corner (paired)
                _LRT_DIRS = {
                    "ללא רק\"ל":                   (0, 0),
                    "צפון-דרום (ישר)":              (1, 0),
                    "מזרח-מערב (ישר)":              (0, 1),
                    "צפון-דרום + כניסה ממזרח":      (2, 0),
                    "צפון-דרום + כניסה ממערב":      (3, 0),
                    "מזרח-מערב + כניסה מצפון":      (0, 2),
                    "מזרח-מערב + כניסה מדרום":      (0, 3),
                    "פנייה צפון ↔ מזרח":            (4, 4),
                    "פנייה מזרח ↔ דרום":            (5, 5),
                    "פנייה דרום ↔ מערב":            (6, 6),
                    "פנייה מערב ↔ צפון":            (7, 7),
                }
                _cur_ns = int(state["instructions"].get("lrt_orig_ns") or 0)
                _cur_ew = int(state["instructions"].get("lrt_orig_ew") or 0)
                _rev = {v: k for k, v in _LRT_DIRS.items()}
                _cur_label = _rev.get((_cur_ns, _cur_ew), "ללא רק\"ל")
                _sel = st.selectbox(
                    "LRT direction type",
                    options=list(_LRT_DIRS.keys()),
                    index=list(_LRT_DIRS.keys()).index(_cur_label),
                    key=f"lrt_dir_sel_{ver}",
                )
                state["instructions"]["lrt_orig_ns"], state["instructions"]["lrt_orig_ew"] = _LRT_DIRS[_sel]

            st.divider()
            st.markdown("**Street names** (Hebrew supported)")
            dir_labels = {"N": "North arm", "S": "South arm",
                          "E": "East arm",  "W": "West arm"}
            for d in DIRECTIONS:
                state["streets"][d] = st.text_input(
                    dir_labels[d],
                    value=str(state["streets"].get(d) or ""),
                    placeholder="שם הרחוב",
                    key=f"st_{d}_{ver}",
                )


# ---------------------------------------------------------------------------
# Run pipeline
# ---------------------------------------------------------------------------
if run_clicked or st.session_state.auto_run:
    st.session_state.auto_run = False
    template = st.session_state.excel_template
    if template is None:
        st.error("Cannot run: volume_calculator.xlsx template missing.")
    else:
        with st.spinner("Running optimization — this may take a few seconds…"):
            try:
                xlsx_bytes = create_excel_from_state(state, template)
                diagram_b, table_b, id_b, queue_b, extra_data = run_pipeline(
                    BytesIO(xlsx_bytes),
                    queue_params=dict(st.session_state.queue_params),
                )
                st.session_state.results    = (diagram_b, table_b, id_b, queue_b)
                st.session_state.extra_data = extra_data
                st.session_state.queue_recalc         = None
                st.session_state.hcm_delay_results    = None
                st.session_state.hcm_queue95_results  = None
                st.session_state.full_zip             = None
                st.success("Analysis complete! Download results from the sidebar.")
                log = extra_data.get("log", "")
                if log.strip():
                    with st.expander("Analysis log"):
                        st.code(log, language="")
                st.rerun()
            except PipelineError as pe:
                st.error(f"Analysis failed: {pe.original_exc}")
                if pe.log.strip():
                    with st.expander("Analysis log (output before error)"):
                        st.code(pe.log, language="")
                with st.expander("Full traceback"):
                    st.exception(pe.original_exc)
            except Exception as exc:
                st.error(f"Analysis failed: {exc}")
                with st.expander("Full error details"):
                    st.exception(exc)


# ---------------------------------------------------------------------------
# ── ADDITIONAL ANALYSIS ─────────────────────────────────────────────────────
# ---------------------------------------------------------------------------
st.divider()
st.header("Additional Analysis")
st.caption(
    "Queue Length recalculation requires a prior Analysis run. "
    "HCM Delay and 95th Queue only need volumes and green times."
)

_dir_labels = {"N": "North", "S": "South", "E": "East", "W": "West"}
hp = st.session_state.hcm_params

# ── Shared inputs for HCM analyses ───────────────────────────────────────────
_aa_left, _aa_right = st.columns([5, 5], gap="large")

with _aa_left:
    st.markdown("**Effective green time per approach (seconds)**")
    gt = st.session_state.hcm_green_times
    _gt_cols = st.columns(4)
    for _col, _d in zip(_gt_cols, ["N", "S", "E", "W"]):
        with _col:
            st.caption(f"**{_dir_labels[_d]}**")
            gt[_d]["am"] = st.number_input(
                "AM (s)", value=int(gt[_d]["am"]),
                min_value=0, max_value=max(10, int(hp.get("cycle_time", 120)) - 1),
                step=1, key=f"gt_{_d}_am",
            )
            gt[_d]["pm"] = st.number_input(
                "PM (s)", value=int(gt[_d]["pm"]),
                min_value=0, max_value=max(10, int(hp.get("cycle_time", 120)) - 1),
                step=1, key=f"gt_{_d}_pm",
            )

with _aa_right:
    st.markdown("**Shared HCM parameters**")
    _p1, _p2, _p3 = st.columns(3)
    with _p1:
        hp["cycle_time"] = st.number_input(
            "Cycle time (s)", value=int(hp.get("cycle_time", 120)),
            min_value=10, step=5, key="hcm_ct",
        )
        hp["saturation_flow"] = st.number_input(
            "Sat. flow (veh/h/lane)", value=int(hp.get("saturation_flow", 1800)),
            min_value=100, step=100, key="hcm_sf",
        )
    with _p2:
        hp["T"] = st.number_input(
            "Analysis period T (hr)", value=float(hp.get("T", 0.25)),
            min_value=0.05, max_value=1.0, step=0.05, format="%.2f", key="hcm_T",
        )
        hp["k"] = st.number_input(
            "k factor", value=float(hp.get("k", 0.5)),
            min_value=0.04, max_value=0.5, step=0.01, format="%.2f", key="hcm_k",
            help="Incremental delay factor: 0.5 pre-timed, 0.25 actuated.",
        )
    with _p3:
        hp["I"] = st.number_input(
            "Upstream filter I", value=float(hp.get("I", 1.0)),
            min_value=0.0, max_value=1.0, step=0.1, format="%.1f", key="hcm_I",
        )
        hp["l"] = st.number_input(
            "Car length l (m)", value=int(hp.get("l", 7)),
            min_value=1, step=1, key="hcm_l",
            help="Used for 95th percentile queue length in metres.",
        )

st.divider()


# ── 1. Queue Length — Poisson Method ─────────────────────────────────────────
with st.expander("📏 Queue Length — Poisson Method", expanded=False):
    has_run = st.session_state.extra_data is not None
    if not has_run:
        st.info("Run the full Analysis first to enable queue recalculation.")

    qp = st.session_state.queue_params
    qc1, qc2, qc3 = st.columns(3)
    with qc1:
        qp["discard_green_time"] = st.checkbox(
            "Discard green time",
            value=bool(qp.get("discard_green_time", False)),
            key="q_dgt",
            help="Multiply queue by the red-time ratio of the relevant movements.",
        )
        qp["basic_lost_capacity"] = st.number_input(
            "Basic lost capacity (veh/h)",
            value=int(qp.get("basic_lost_capacity", 200)),
            min_value=0, step=50, key="q_blc",
        )
    with qc2:
        qp["poisson"] = st.number_input(
            "Poisson percentile",
            value=float(qp.get("poisson", 0.95)),
            min_value=0.50, max_value=0.99, step=0.01, format="%.2f",
            key="q_poi",
        )
        qp["phf"] = st.number_input(
            "PHF — peak hour factor",
            value=float(qp.get("phf", 0.9)),
            min_value=0.1, max_value=1.0, step=0.05, format="%.2f",
            key="q_phf",
        )
    with qc3:
        qp["l"] = st.number_input(
            "Car length — l (m)",
            value=int(qp.get("l", 7)),
            min_value=1, step=1, key="q_l",
        )
        qp["cycle_time"] = st.number_input(
            "Cycle time (s)",
            value=int(qp.get("cycle_time", 120)),
            min_value=10, step=5, key="q_ct",
        )

    if st.button("🔄 Recalculate Queue", disabled=not has_run, key="btn_q_recalc"):
        try:
            ed   = st.session_state.extra_data
            _qpd = dict(qp)
            q_am = _queue_length(ed["car_sum_am"], ed["pulp_vars_am"], **_qpd)
            q_pm = _queue_length(ed["car_sum_pm"], ed["pulp_vars_pm"], **_qpd)
            q_max = [max(a, b) for a, b in zip(q_am, q_pm)]
            st.session_state.queue_recalc = {
                "car_length_dict": dict(zip(_QUEUE_NAMES, q_max)),
                "params": _qpd,
            }
            st.rerun()
        except Exception as exc:
            st.error(f"Recalculation failed: {exc}")

    # Determine which queue results to display
    _cd = None
    _qp_used = None
    if st.session_state.queue_recalc:
        _cd      = st.session_state.queue_recalc["car_length_dict"]
        _qp_used = st.session_state.queue_recalc["params"]
        st.success("Showing recalculated results.")
    elif has_run:
        _cd      = st.session_state.extra_data.get("car_length_dict")
        _qp_used = dict(qp)
        st.caption("Showing results from last Analysis run.")

    if _cd is not None:
        _q_rows = []
        for _d in ["N", "S", "E", "W"]:
            for _m in ["R", "RT", "T", "TL", "L", "RTL", "RL"]:
                _key = f"{_d}{_m}_length"
                _len = _cd.get(_key, 0)
                if _len > 0:
                    _q_rows.append({
                        "Direction": _DIR_EN[_d],
                        "Movement":  _MOVE_EN[_m],
                        "Queue (m)": _len,
                    })
        if _q_rows:
            st.dataframe(pd.DataFrame(_q_rows), use_container_width=True, hide_index=True)
        else:
            st.info("All queue lengths are zero.")

        _qxl = make_queue_excel(_cd, _qp_used)
        st.download_button(
            "⬇ Download Queue Results",
            _qxl, "QueueLengths.xlsx", XLSX_MIME,
            key="dl_q_recalc",
        )


# ── 2. HCM Signal Delay & Level of Service ───────────────────────────────────
with st.expander("⏱ HCM Signal Delay & Level of Service (Experimental)", expanded=False):
    st.caption(
        "Uses volumes from the form above, green times, and shared HCM parameters. "
        "d1 = uniform delay (Webster), d2 = overflow delay — HCM 7th ed. methodology."
    )
    _hp_delay = dict(hp)
    _pf_col, _ = st.columns([2, 4])
    with _pf_col:
        _hp_delay["PF"] = st.number_input(
            "Progression factor PF", value=float(hp.get("PF", 1.0)),
            min_value=0.1, max_value=2.0, step=0.05, format="%.2f",
            key="hd_pf",
            help="Arrival-type progression adjustment (1.0 = random arrivals).",
        )

    if st.button("📐 Calculate Delay & LOS", key="btn_hcm_delay"):
        try:
            st.session_state.hcm_delay_results = compute_hcm_delay(
                state, st.session_state.hcm_green_times, _hp_delay
            )
            # store PF back into shared params
            hp["PF"] = _hp_delay["PF"]
            st.rerun()
        except Exception as exc:
            st.error(f"Calculation failed: {exc}")

    if st.session_state.hcm_delay_results:
        dr = st.session_state.hcm_delay_results
        _d_rows = []
        for _d in ["N", "S", "E", "W"]:
            for _period, _label in [("morning", "AM"), ("evening", "PM")]:
                _r = dr[_d][_period]
                _d_rows.append({
                    "Direction":     _dir_labels[_d],
                    "Period":        _label,
                    "Green (s)":     _r["g"],
                    "Volume (v/h)":  _r["v"],
                    "Capacity":      _r["c"],
                    "X (v/c)":       _r["X"],
                    "d1 (s)":        _r["d1"],
                    "d2 (s)":        _r["d2"],
                    "Delay (s/veh)": _r["delay"],
                    "LOS":           _r["LOS"],
                })
        _df_d = pd.DataFrame(_d_rows)

        _los_bg = {
            "A": "#C6EFCE", "B": "#FFEB9C", "C": "#FFC7CE",
            "D": "#FF9999", "E": "#FF6666", "F": "#CC2200",
        }
        def _style_los(val):
            return (f"background-color: {_los_bg.get(val, '')}; "
                    f"color: {'white' if val in ('E','F') else 'black'}")

        st.dataframe(
            _df_d.style.applymap(_style_los, subset=["LOS"]),
            use_container_width=True, hide_index=True,
        )

        _hq95_for_dl = st.session_state.hcm_queue95_results or compute_hcm_queue95(
            state, st.session_state.hcm_green_times, dict(hp)
        )
        _hxl = make_hcm_excel(dr, _hq95_for_dl, st.session_state.hcm_green_times, dict(hp))
        st.download_button(
            "⬇ Download HCM Results (Delay + Queue)",
            _hxl, "HCM_Analysis.xlsx", XLSX_MIME,
            key="dl_hcm_delay",
        )


# ── 3. HCM 95th Percentile Queue ─────────────────────────────────────────────
with st.expander("📊 HCM 95th Percentile Back-of-Queue (Experimental)", expanded=False):
    st.caption(
        "Uses volumes, green times, and shared HCM parameters. "
        "Nq = Nq1 (uniform) + Nq2 (overflow).  Q95 = Nq + 1.65·√Nq  — HCM 7th ed. methodology."
    )

    if st.button("📊 Calculate 95th Queue", key="btn_hcm_q95"):
        try:
            st.session_state.hcm_queue95_results = compute_hcm_queue95(
                state, st.session_state.hcm_green_times, dict(hp)
            )
            st.rerun()
        except Exception as exc:
            st.error(f"Calculation failed: {exc}")

    if st.session_state.hcm_queue95_results:
        qr = st.session_state.hcm_queue95_results
        _q_rows2 = []
        for _d in ["N", "S", "E", "W"]:
            for _period, _label in [("morning", "AM"), ("evening", "PM")]:
                _r = qr[_d][_period]
                _q_rows2.append({
                    "Direction":       _dir_labels[_d],
                    "Period":          _label,
                    "Green (s)":       _r["g"],
                    "Volume (v/h)":    _r["v"],
                    "Capacity":        _r["c"],
                    "X (v/c)":         _r["X"],
                    "Avg Queue (veh)": _r["Nq"],
                    "Q95 (veh)":       _r["Q95_veh"],
                    "Q95 (m)":         _r["Q95_m"],
                })
        st.dataframe(
            pd.DataFrame(_q_rows2), use_container_width=True, hide_index=True,
        )

        _hd_for_dl = st.session_state.hcm_delay_results or compute_hcm_delay(
            state, st.session_state.hcm_green_times,
            {**dict(hp), "PF": hp.get("PF", 1.0)},
        )
        _hxl2 = make_hcm_excel(_hd_for_dl, qr, st.session_state.hcm_green_times, dict(hp))
        st.download_button(
            "⬇ Download HCM Results (Delay + Queue)",
            _hxl2, "HCM_Analysis.xlsx", XLSX_MIME,
            key="dl_hcm_q95",
        )
