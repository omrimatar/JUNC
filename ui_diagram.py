"""
ui_diagram.py — Matplotlib live junction schematic for the JUNC Streamlit UI.

draw_junction(state) returns a matplotlib Figure.  Each road arm shows
per-movement (R / T / L) volume bars:
  • Solid bar  = AM (morning)
  • Faded bar  = PM (evening)
  • Green = Right turn  |  Blue = Through  |  Orange = Left turn
"""

import platform
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe

from ui_excel import DIRECTIONS

# ── Font ──────────────────────────────────────────────────────────────────────
_FONT = "Tahoma" if platform.system() == "Windows" else "DejaVu Sans"


def _rtl(text: str) -> str:
    """Reorder Hebrew/Arabic text for correct RTL display in matplotlib."""
    if not text:
        return text
    try:
        from bidi.algorithm import get_display
        return get_display(text)
    except ImportError:
        # Fallback: reverse if string contains Hebrew/Arabic characters
        if any('\u0590' <= c <= '\u05ff' or '\u0600' <= c <= '\u06ff' for c in text):
            return text[::-1]
        return text

# ── Layout ────────────────────────────────────────────────────────────────────
_ROAD_HW  = 1.15   # half-width of road arm
_BOX      = 1.15   # half-size of intersection square
_EXTENT   = 5.5    # axis extent

# Bar chart geometry (in data-unit space)
_BAR_W      = 0.20   # width of one bar (AM or PM)
_BAR_GAP    = 0.05   # gap between AM and PM within one group
_GROUP_SEP  = 0.62   # centre-to-centre distance between R / T / L groups
_MAX_LEN    = 1.85   # max bar length (full scale)
_MIN_LEN    = 0.04   # minimum visible length for non-zero volumes

_STREET_R = 4.75     # distance from origin for street-name text

# ── Colours ───────────────────────────────────────────────────────────────────
_BG      = "#1c1c2b"
_ROAD    = "#3b3b4f"
_DIVIDER = "#555577"

# Movement colours  (R=green, T=sky-blue, L=orange)
_MC = {"R": "#66bb6a", "T": "#4fc3f7", "L": "#ffa726"}

# Per-movement screen offsets (perpendicular to arm direction)
# Order: R at +_GROUP_SEP, T at 0, L at -_GROUP_SEP
_PERP = {"R": +_GROUP_SEP, "T": 0.0, "L": -_GROUP_SEP}

_DIR_UNIT = {"N": (0, 1), "S": (0, -1), "E": (1, 0), "W": (-1, 0)}

_STREET_COLOR = "#ffe082"
_DIR_COLOR    = "#8888aa"

# Lane type colours (right → left order)
_LANE_ORDER = ["R", "RT", "T", "TL", "L", "RTL", "RL"]
_LC = {
    "R":   "#66bb6a",
    "RT":  "#9dd474",
    "T":   "#4fc3f7",
    "TL":  "#66c9c0",
    "L":   "#ffa726",
    "RTL": "#c0b0f0",
    "RL":  "#b0d880",
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _arm_rect(dx, dy):
    if dy ==  1: return (-_ROAD_HW, _BOX,     2*_ROAD_HW, _EXTENT - _BOX)
    if dy == -1: return (-_ROAD_HW, -_EXTENT, 2*_ROAD_HW, _EXTENT - _BOX)
    if dx ==  1: return ( _BOX,    -_ROAD_HW, _EXTENT - _BOX, 2*_ROAD_HW)
    return              (-_EXTENT, -_ROAD_HW, _EXTENT - _BOX, 2*_ROAD_HW)


def _global_max(state):
    """Return the maximum single-movement volume across all directions & periods."""
    vmax = 1
    for period in ("morning", "evening"):
        for d in DIRECTIONS:
            for v in state.get("volumes", {}).get(period, {}).get(d, {}).values():
                if (v or 0) > vmax:
                    vmax = v
    return vmax


def _bar_len(vol, vmax):
    if not vol:
        return 0.0
    return max(_MIN_LEN, (vol / vmax) * _MAX_LEN)


# ── Lane stripes ──────────────────────────────────────────────────────────────

def _draw_lane_stripes(ax, state, d):
    """Draw lane dividers and per-lane type labels for one arm."""
    lanes_d = state.get("lanes", {}).get(d, {})
    lane_list = []
    for lt in _LANE_ORDER:
        for _ in range(int(lanes_d.get(lt, 0) or 0)):
            lane_list.append(lt)
    n = len(lane_list)
    if n == 0:
        return

    dx, dy = _DIR_UNIT[d]
    lane_w = 2 * _ROAD_HW / n

    # Subtle divider lines between lanes
    for i in range(1, n):
        perp = _ROAD_HW - lane_w * i
        if dy != 0:
            y0, y1 = (_BOX, _EXTENT) if dy > 0 else (-_EXTENT, -_BOX)
            ax.plot([perp, perp], [y0, y1],
                    color=_DIVIDER, lw=0.55, ls="--", alpha=0.55, zorder=3)
        else:
            x0, x1 = (_BOX, _EXTENT) if dx > 0 else (-_EXTENT, -_BOX)
            ax.plot([x0, x1], [perp, perp],
                    color=_DIVIDER, lw=0.55, ls="--", alpha=0.55, zorder=3)

    # Lane type label just past the stop line, centred in each lane strip
    label_dist = _BOX + 0.32
    for i, lt in enumerate(lane_list):
        perp = _ROAD_HW - lane_w * (i + 0.5)
        color = _LC.get(lt, "#aaaaaa")
        lx, ly = (perp, label_dist * dy) if dy != 0 else (label_dist * dx, perp)
        ax.text(lx, ly, lt,
                color=color, fontsize=4.5, ha="center", va="center",
                fontweight="bold", zorder=8,
                bbox=dict(boxstyle="round,pad=0.08", fc=_BG, ec=color, lw=0.5, alpha=0.92))


# ── Per-arm bar drawing ───────────────────────────────────────────────────────

def _draw_arm(ax, state, d, vmax):
    """Draw R/T/L AM+PM volume bars for one arm."""
    dx, dy = _DIR_UNIT[d]
    vols_am = state.get("volumes", {}).get("morning", {}).get(d, {})
    vols_pm = state.get("volumes", {}).get("evening", {}).get(d, {})

    for m in ("R", "T", "L"):
        perp  = _PERP[m]          # offset perpendicular to arm axis
        color = _MC[m]
        am    = int(vols_am.get(m, 0) or 0)
        pm    = int(vols_pm.get(m, 0) or 0)
        am_l  = _bar_len(am, vmax)
        pm_l  = _bar_len(pm, vmax)

        # ── Bar rectangles ────────────────────────────────────────────────────
        # AM bar: solid (alpha=0.90), slightly inward (toward axis)
        # PM bar: faded (alpha=0.45), slightly outward
        half_g = (_BAR_GAP + _BAR_W) / 2   # distance from group centre to bar centre

        if dy != 0:
            # N / S arm — bars are vertical
            am_bx = perp - half_g - _BAR_W/2  # left edge of AM bar
            pm_bx = perp + _BAR_GAP/2          # left edge of PM bar
            base  = _BOX * dy                  # intersection edge y
            if dy > 0:   # N: grow upward
                ax.add_patch(mpatches.Rectangle(
                    (am_bx, base), _BAR_W,  am_l,
                    facecolor=color, alpha=0.90, zorder=5, lw=0.3, ec="white"))
                ax.add_patch(mpatches.Rectangle(
                    (pm_bx, base), _BAR_W,  pm_l,
                    facecolor=color, alpha=0.40, zorder=5, lw=0.3, ec="white"))
                # Volume labels at bar tips
                _vlabel(ax, am_bx + _BAR_W/2, base + am_l, am, color, "center",
                        "bottom", 1.0)
                _vlabel(ax, pm_bx + _BAR_W/2, base + pm_l, pm, color, "center",
                        "bottom", 0.55)
            else:          # S: grow downward
                ax.add_patch(mpatches.Rectangle(
                    (am_bx, base - am_l), _BAR_W, am_l,
                    facecolor=color, alpha=0.90, zorder=5, lw=0.3, ec="white"))
                ax.add_patch(mpatches.Rectangle(
                    (pm_bx, base - pm_l), _BAR_W, pm_l,
                    facecolor=color, alpha=0.40, zorder=5, lw=0.3, ec="white"))
                _vlabel(ax, am_bx + _BAR_W/2, base - am_l, am, color, "center",
                        "top", 1.0)
                _vlabel(ax, pm_bx + _BAR_W/2, base - pm_l, pm, color, "center",
                        "top", 0.55)

        else:
            # E / W arm — bars are horizontal
            am_by = perp - half_g - _BAR_W/2
            pm_by = perp + _BAR_GAP/2
            base  = _BOX * dx
            if dx > 0:   # E: grow rightward
                ax.add_patch(mpatches.Rectangle(
                    (base, am_by), am_l, _BAR_W,
                    facecolor=color, alpha=0.90, zorder=5, lw=0.3, ec="white"))
                ax.add_patch(mpatches.Rectangle(
                    (base, pm_by), pm_l, _BAR_W,
                    facecolor=color, alpha=0.40, zorder=5, lw=0.3, ec="white"))
                _vlabel(ax, base + am_l, am_by + _BAR_W/2, am, color, "left",
                        "center", 1.0)
                _vlabel(ax, base + pm_l, pm_by + _BAR_W/2, pm, color, "left",
                        "center", 0.55)
            else:          # W: grow leftward
                ax.add_patch(mpatches.Rectangle(
                    (base - am_l, am_by), am_l, _BAR_W,
                    facecolor=color, alpha=0.90, zorder=5, lw=0.3, ec="white"))
                ax.add_patch(mpatches.Rectangle(
                    (base - pm_l, pm_by), pm_l, _BAR_W,
                    facecolor=color, alpha=0.40, zorder=5, lw=0.3, ec="white"))
                _vlabel(ax, base - am_l, am_by + _BAR_W/2, am, color, "right",
                        "center", 1.0)
                _vlabel(ax, base - pm_l, pm_by + _BAR_W/2, pm, color, "right",
                        "center", 0.55)

        # ── Movement letter at bar base (just inside intersection edge) ───────
        letter_offset = 0.18   # inset from intersection edge
        if dy != 0:
            lx = perp
            ly = (_BOX - letter_offset) * dy
        else:
            lx = (_BOX - letter_offset) * dx
            ly = perp
        ax.text(lx, ly, m, color=color, fontsize=5.5, ha="center", va="center",
                fontweight="bold", alpha=0.75, zorder=6)


def _vlabel(ax, x, y, vol, color, ha, va, alpha):
    """Tiny volume number label at a bar tip, only when vol > 0."""
    if not vol:
        return
    # nudge slightly away from bar tip
    ax.text(x, y, str(vol), color=color, fontsize=5.5,
            ha=ha, va=va, alpha=alpha, zorder=7,
            path_effects=[pe.withStroke(linewidth=1.5, foreground=_BG)])


# ── Main draw function ────────────────────────────────────────────────────────

def draw_junction(state: dict) -> plt.Figure:
    """
    Draw a top-view traffic junction schematic with per-movement (R/T/L)
    volume bar charts on each arm.

    Returns a matplotlib Figure.
    """
    matplotlib.rcParams["font.family"] = _FONT

    fig, ax = plt.subplots(figsize=(6.2, 6.2), facecolor=_BG)
    ax.set_facecolor(_BG)
    ax.set_xlim(-_EXTENT, _EXTENT)
    ax.set_ylim(-_EXTENT, _EXTENT)
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Road geometry ─────────────────────────────────────────────────────────
    for d in DIRECTIONS:
        dx, dy = _DIR_UNIT[d]
        x, y, w, h = _arm_rect(dx, dy)
        ax.add_patch(mpatches.Rectangle((x, y), w, h, facecolor=_ROAD, zorder=1))

    ax.add_patch(mpatches.Rectangle(
        (-_BOX, -_BOX), 2*_BOX, 2*_BOX, facecolor=_ROAD, zorder=2))

    dash = dict(color=_DIVIDER, ls="--", lw=0.8, alpha=0.55, zorder=3)
    ax.plot([0, 0], [_BOX,  _EXTENT], **dash)
    ax.plot([0, 0], [-_EXTENT, -_BOX], **dash)
    ax.plot([_BOX,  _EXTENT],   [0, 0], **dash)
    ax.plot([-_EXTENT, -_BOX], [0, 0], **dash)

    # ── Lane stripes (drawn before bars so bars sit on top) ───────────────────
    for d in DIRECTIONS:
        _draw_lane_stripes(ax, state, d)

    # ── Volume bars ───────────────────────────────────────────────────────────
    vmax = _global_max(state)
    for d in DIRECTIONS:
        _draw_arm(ax, state, d, vmax)

    # ── Street names ──────────────────────────────────────────────────────────
    streets = state.get("streets", {})
    for d in DIRECTIONS:
        dx, dy = _DIR_UNIT[d]
        street = str(streets.get(d, "") or "").strip()
        label  = _rtl(street) if street else d
        color  = _STREET_COLOR if street else _DIR_COLOR
        style  = "normal"  if street else "italic"
        size   = 8         if street else 7

        ax.text(dx * _STREET_R, dy * _STREET_R, label,
                color=color, fontsize=size, fontstyle=style,
                fontweight="semibold", ha="center", va="center", zorder=5,
                path_effects=[pe.withStroke(linewidth=2.5, foreground=_BG)])

    # ── Directional flow arrows ───────────────────────────────────────────────
    akw = dict(color="#666688", width=0.055, head_width=0.20, head_length=0.15,
               length_includes_head=True, zorder=4, alpha=0.65)
    ofs = _BOX + 0.22
    ax.arrow( 0.18,  ofs,  0,    0.5,  **akw)
    ax.arrow(-0.18, -ofs,  0,   -0.5,  **akw)
    ax.arrow( ofs,  -0.18, 0.5,  0,    **akw)
    ax.arrow(-ofs,   0.18, -0.5, 0,    **akw)

    # ── Title ─────────────────────────────────────────────────────────────────
    proj = str(state.get("junc", {}).get("more_info", "") or "").strip()
    ax.set_title(_rtl(proj) if proj else "Junction Schematic",
                 color="#ccccdd", fontsize=9.5, pad=10, fontweight="bold")

    # ── Legend ────────────────────────────────────────────────────────────────
    legend_handles = [
        mpatches.Patch(facecolor=_MC["R"], label="R  right turn"),
        mpatches.Patch(facecolor=_MC["T"], label="T  through"),
        mpatches.Patch(facecolor=_MC["L"], label="L  left turn"),
        mpatches.Patch(facecolor="#888888", alpha=0.90, label="solid = AM"),
        mpatches.Patch(facecolor="#888888", alpha=0.40, label="faded = PM"),
    ]
    ax.legend(handles=legend_handles, loc="lower center",
              ncol=5, framealpha=0.0, labelcolor="white",
              fontsize=6, handlelength=0.9,
              bbox_to_anchor=(0.5, -0.06))

    fig.tight_layout(pad=0.4)
    return fig
