"""
test_edge_cases.py - Edge-case validation test suite for JUNC.

Runs b_optimization and Phaser validation with invalid inputs.
MessageBox calls are intercepted so no Windows dialogs appear.
SystemExit (from exit()) is caught and reported.

Usage:  python test_edge_cases.py
"""

import ctypes
import sys
import os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')
from unittest.mock import patch

# -- Base valid inputs ----------------------------------------------------------
# volume: [NR,NT,NL, SR,ST,SL, ER,ET,EL, WR,WT,WL]
BASE_VOLUME = [100, 300, 150,   100, 300, 150,   100, 300, 150,   100, 300, 150]

# lanes per direction: [R, RT, T, TL, L, RTL, RL]
# R=1, T=2, L=1 for each direction
BASE_LANES  = [1,0,2,0,1,0,0,  1,0,2,0,1,0,0,  1,0,2,0,1,0,0,  1,0,2,0,1,0,0]

# nataz: all zeros (no restrictions)
BASE_NATAZ  = [0]*28

BASE_SOLVER = 1

PASS  = "PASS "
FAIL  = "FAIL "
ERROR = "ERROR"

results = []

def run_b(name, volume, lanes, nataz, expected_contains=None):
    """Run b_optimization; capture MessageBox message and SystemExit."""
    captured = []

    def fake_msgbox(hwnd, text, caption, flags):
        captured.append(text)
        return 1   # IDOK

    with patch.object(ctypes.windll.user32, 'MessageBoxW', fake_msgbox):
        try:
            from b_optimization import b_optimization
            b_optimization(volume, lanes, nataz, BASE_SOLVER)
            msg = "(no error raised)"
            status = PASS if expected_contains is None else FAIL
        except SystemExit:
            msg = captured[-1] if captured else "(exit() with no MessageBox)"
            status = PASS if (expected_contains and expected_contains in msg) else FAIL
        except Exception as exc:
            msg = f"Exception: {exc}"
            status = PASS if (expected_contains and expected_contains in str(exc)) else FAIL

    results.append((status, name, msg))
    print(f"{status} | {name}")
    print(f"       msg: {msg}\n")


def run_phaser_read(name, state_override: dict, expected_contains=None):
    """
    Test Phaser.read_from_excel validation by creating an Excel in a tempdir
    and running Phaser.main() with MessageBox mocked.
    """
    import tempfile, shutil
    from ui_excel import create_excel_from_state, default_state

    state = default_state()
    for key, val in state_override.items():
        if isinstance(val, dict):
            for k2, v2 in val.items():
                if isinstance(v2, dict):
                    state[key][k2].update(v2)
                else:
                    state[key][k2] = v2
        else:
            state[key] = val

    # load template
    tmpl_path = os.path.join(os.path.dirname(__file__), "volume_calculator.xlsx")
    if not os.path.exists(tmpl_path):
        results.append((ERROR, name, "template not found"))
        print(f"{ERROR} | {name} - template not found\n")
        return

    with open(tmpl_path, "rb") as f:
        tmpl_bytes = f.read()

    try:
        xlsx_bytes = create_excel_from_state(state, tmpl_bytes)
    except Exception as exc:
        msg = f"create_excel_from_state failed: {exc}"
        status = PASS if (expected_contains and expected_contains in str(exc)) else FAIL
        results.append((status, name, msg))
        print(f"{status} | {name}")
        print(f"       msg: {msg}\n")
        return

    workdir = tempfile.mkdtemp(prefix="junc_test_")
    captured_msg = []

    def fake_msgbox(hwnd, text, caption, flags):
        captured_msg.append(text)
        return 1

    try:
        with open(os.path.join(workdir, "volume_calculator.xlsx"), "wb") as f:
            f.write(xlsx_bytes)
        output_src = os.path.join(os.path.dirname(__file__), "OUTPUT.xlsx")
        if os.path.exists(output_src):
            shutil.copy2(output_src, os.path.join(workdir, "OUTPUT.xlsx"))

        orig_dir = os.getcwd()
        os.chdir(workdir)

        import io, contextlib
        devnull = io.StringIO()
        with patch.object(ctypes.windll.user32, 'MessageBoxW', fake_msgbox):
            try:
                import Phaser
                with contextlib.redirect_stdout(devnull):
                    Phaser.main()
                msg = "(no error raised)"
                status = PASS if expected_contains is None else FAIL
            except SystemExit:
                msg = captured_msg[-1] if captured_msg else "(exit() with no MessageBox)"
                status = PASS if (expected_contains and expected_contains in msg) else FAIL
            except ValueError as exc:
                msg = f"ValueError: {exc}"
                status = PASS if (expected_contains and expected_contains in str(exc)) else FAIL
            except Exception as exc:
                msg = f"Exception({type(exc).__name__}): {exc}"
                status = PASS if (expected_contains and expected_contains in str(exc)) else FAIL
    finally:
        os.chdir(orig_dir)
        shutil.rmtree(workdir, ignore_errors=True)

    results.append((status, name, msg))
    print(f"{status} | {name}")
    print(f"       msg: {msg}\n")


# ===============================================================================
# GROUP A: b_optimization direct tests
# ===============================================================================
print("=" * 70)
print("GROUP A: b_optimization - direct validation tests")
print("=" * 70)

# A1: Valid baseline - should pass
run_b("A1 baseline (valid)", BASE_VOLUME[:], BASE_LANES[:], BASE_NATAZ[:])

# A2: Volume with no lane for that movement (NR>0 but no R/RT/RL/RTL lane N)
lanes_no_nr = BASE_LANES[:]
lanes_no_nr[0] = 0   # NlanesR=0 (also no RT/RTL/RL in base)
run_b("A2 NR volume but no N-right lane",
      BASE_VOLUME[:], lanes_no_nr, BASE_NATAZ[:],
      expected_contains="North right-turn volume")

# A3: NRT=1 AND NTL=1 in same direction - are these two different complex types allowed?
# The validation only fires if a SINGLE complex type count > 1 (e.g., NRT=2)
# NRT=1 + NTL=1 is actually valid (T traffic splits across RT and TL lanes)
lanes_two_complex = BASE_LANES[:]
lanes_two_complex[1] = 1   # NRT=1
lanes_two_complex[3] = 1   # NTL=1
run_b("A3 NRT=1 AND NTL=1 (two different complex types - valid combo, no error expected)",
      BASE_VOLUME[:], lanes_two_complex, BASE_NATAZ[:])  # no error expected

# A3b: Single complex type count > 1 (NRT=2) - SHOULD be caught
lanes_nrt2 = BASE_LANES[:]
lanes_nrt2[1] = 2   # NRT=2 (invalid: only 1 complex lane allowed per type)
run_b("A3b NlanesRT=2 (single complex type > 1 - invalid)",
      BASE_VOLUME[:], lanes_nrt2, BASE_NATAZ[:],
      expected_contains="North routing error")

# A4: Non-integer lane value (float)
lanes_float = BASE_LANES[:]
lanes_float[2] = 1.5  # NT = 1.5
run_b("A4 float lane value (NT=1.5)",
      BASE_VOLUME[:], lanes_float, BASE_NATAZ[:],
      expected_contains="integer")

# A5: Invalid nataz code for RT (>3)
nataz_bad_rt = BASE_NATAZ[:]
nataz_bad_rt[1] = 5  # NRT nataz = 5 (max is 3)
run_b("A5 nataz[1] (N-RT) = 5 (invalid, max=3)",
      BASE_VOLUME[:], BASE_LANES[:], nataz_bad_rt,
      expected_contains="nataz")

# A6: Invalid nataz code for TL (=2, forbidden)
nataz_bad_tl = BASE_NATAZ[:]
nataz_bad_tl[3] = 2  # NTL nataz = 2 (forbidden)
run_b("A6 nataz[3] (N-TL) = 2 (forbidden value)",
      BASE_VOLUME[:], BASE_LANES[:], nataz_bad_tl,
      expected_contains="nataz")

# A7: nataz blocks all lanes for a movement that has volume
# NTL lane exists, nataz[3]=3 (no T on TL), NT=0 -> no T lane at all
lanes_only_tl = BASE_LANES[:]
lanes_only_tl[2] = 0   # no NlanesT
lanes_only_tl[3] = 1   # NlanesTL=1
nataz_tl_no_t = BASE_NATAZ[:]
nataz_tl_no_t[3] = 3   # disable T on TL
vol_nt = BASE_VOLUME[:]
vol_nt[1] = 500  # NcountT = 500
run_b("A7 NTL only, nataz blocks T, NcountT>0 -> missing north through",
      vol_nt, lanes_only_tl, nataz_tl_no_t,
      expected_contains="North through volume")

# A8: RL lane + T lane conflict (RL and T both present, forbidden combination)
# The LP will set NtrafficRLr and NtrafficRLl but T-through traffic has nowhere to go
# This is NOT caught by upfront validation - it just becomes LP infeasible
lanes_rl_t = BASE_LANES[:]
lanes_rl_t[2] = 2   # NlanesT=2
lanes_rl_t[6] = 1   # NlanesRL=1 (RL+T is invalid: no T-movement path through RL lane)
run_b("A8 N-RL + N-T lanes together (LP should fail - T has no route via RL)",
      BASE_VOLUME[:], lanes_rl_t, BASE_NATAZ[:])

# A9: Missing south left turn (ScountL>0 but no S-left-capable lane)
vol_sl = BASE_VOLUME[:]
vol_sl[5] = 200  # ScountL = 200
lanes_no_sl = BASE_LANES[:]
lanes_no_sl[11] = 0  # SlanesL=0
lanes_no_sl[10] = 0  # SlanesTL=0
lanes_no_sl[12] = 0  # SlanesRTL=0
lanes_no_sl[13] = 0  # SlanesRL=0
run_b("A9 ScountL>0 but no south left lane",
      vol_sl, lanes_no_sl, BASE_NATAZ[:],
      expected_contains="South left-turn volume")

# A10: RTL with nataz blocking all movements (nataz=7 -> blocks R+T+L)
lanes_rtl = BASE_LANES[:]
lanes_rtl[2] = 0   # remove plain T
lanes_rtl[4] = 0   # remove plain L
lanes_rtl[5] = 1   # NRTL=1
nataz_rtl_all = BASE_NATAZ[:]
nataz_rtl_all[5] = 7  # block R+T+L on NRTL
run_b("A10 NRTL only, nataz=7 blocks all movements",
      BASE_VOLUME[:], lanes_rtl, nataz_rtl_all,
      expected_contains="North through volume")

# A11: Negative volume
vol_neg = BASE_VOLUME[:]
vol_neg[0] = -50  # NcountR = -50
run_b("A11 negative volume (NR=-50)",
      vol_neg, BASE_LANES[:], BASE_NATAZ[:],
      expected_contains="Negative volume")

# A12: All zero volumes - should pass trivially
run_b("A12 all zero volumes",
      [0]*12, BASE_LANES[:], BASE_NATAZ[:])

# A13: Extremely large volume (10000) with only 1 T lane - LP might be infeasible
vol_huge = [0]*12
vol_huge[1] = 10000  # NcountT = 10000
lanes_one_t = [0]*28
lanes_one_t[2] = 1   # NlanesT=1
run_b("A13 extreme volume NcountT=10000 with 1 T lane - LP may fail",
      vol_huge, lanes_one_t, BASE_NATAZ[:])

# A14: All lanes zero but volume exists
vol_only = [0]*12
vol_only[1] = 300  # NcountT=300
lanes_all_zero = [0]*28
run_b("A14 all lanes=0 but NcountT>0 - missing north through",
      vol_only, lanes_all_zero, BASE_NATAZ[:],
      expected_contains="North through volume")

# A15: nataz RL = 3 (forbidden)
nataz_rl_bad = BASE_NATAZ[:]
nataz_rl_bad[6] = 3  # NRL nataz = 3 (forbidden)
run_b("A15 nataz[6] (N-RL) = 3 (forbidden)",
      BASE_VOLUME[:], BASE_LANES[:], nataz_rl_bad,
      expected_contains="nataz")

# A16: nataz RTL = 8 (>7, invalid)
nataz_rtl_bad = BASE_NATAZ[:]
nataz_rtl_bad[5] = 8  # NRTL nataz = 8 (max is 7)
run_b("A16 nataz[5] (N-RTL) = 8 (max=7)",
      BASE_VOLUME[:], BASE_LANES[:], nataz_rtl_bad,
      expected_contains="nataz")

# A17: TL nataz=4 (disable L on TL) with WL volume but only WTL lane
lanes_w_tl = BASE_LANES[:]
lanes_w_tl[25] = 0   # WlanesL=0
lanes_w_tl[24] = 1   # WlanesTL=1
nataz_w_tl4 = BASE_NATAZ[:]
nataz_w_tl4[24] = 4  # disable L on WTL
vol_wl = BASE_VOLUME[:]
vol_wl[11] = 200     # WcountL=200
run_b("A17 WTL only, nataz=4 disables L, WcountL>0 -> missing west left",
      vol_wl, lanes_w_tl, nataz_w_tl4,
      expected_contains="West left-turn volume")

# A18: south complex lane count > 1 (SRT=2)
lanes_srt2 = BASE_LANES[:]
lanes_srt2[8] = 2   # SlanesRT=2
run_b("A18 SlanesRT=2 (>1 complex lane south)",
      BASE_VOLUME[:], lanes_srt2, BASE_NATAZ[:],
      expected_contains="South routing error")

# ===============================================================================
# GROUP B: Phaser.py type/value validation (via full Phaser.main)
# ===============================================================================
print("=" * 70)
print("GROUP B: Phaser.main - type and value validation")
print("=" * 70)

# B1: Non-integer instruction (capacity as string)
run_phaser_read("B1 instruction capacity='abc' (non-integer)",
    {"instructions": {"capacity": "abc"}},
    expected_contains="integers")

# B2: Inflation = 0 -> should raise error
run_phaser_read("B2 inflation=0 -> invalid (must be > 0)",
    {"instructions": {"inflation": 0}},
    expected_contains="Invalid inflation factor")

# B3: Inflation = negative -> should raise error
run_phaser_read("B3 inflation=-1 -> invalid (must be > 0)",
    {"instructions": {"inflation": -1}},
    expected_contains="Invalid inflation factor")

# B3b: Inflation = -1 with real volumes -> should raise error
run_phaser_read("B3b inflation=-1 with real volumes -> invalid",
    {"instructions": {"inflation": -1.0},
     "volumes": {
         "morning": {"N": {"R": 100, "T": 300, "L": 150},
                     "S": {"R": 100, "T": 300, "L": 150},
                     "E": {"R": 100, "T": 300, "L": 150},
                     "W": {"R": 100, "T": 300, "L": 150}},
         "evening": {"N": {"R": 100, "T": 300, "L": 150},
                     "S": {"R": 100, "T": 300, "L": 150},
                     "E": {"R": 100, "T": 300, "L": 150},
                     "W": {"R": 100, "T": 300, "L": 150}},
     },
     "lanes": {d: {"R": 1, "T": 2, "L": 1} for d in ["N", "S", "E", "W"]}
    },
    expected_contains="Invalid inflation factor")

# B4: Inflation = None (falsy -> default to 1.0)
run_phaser_read("B4 inflation=None -> defaults to 1.0 (safe)",
    {"instructions": {"inflation": None}})

# B5: Rakal instruction non-integer
run_phaser_read("B5 rakal cycle_time='x' (non-integer)",
    {"rakal": {"cycle_time": "x"}},
    expected_contains="integers")

# B6: Non-numeric volume - inject directly into Excel bypassing ui_excel int() cast
def run_b6_raw_excel(name, cell_row, cell_col, bad_value, expected_contains=None):
    """Write a bad value directly into a cell of the Excel template and run Phaser."""
    import tempfile, shutil, io, contextlib
    from io import BytesIO
    import openpyxl as xl2
    tmpl_path = os.path.join(os.path.dirname(__file__), "volume_calculator.xlsx")
    if not os.path.exists(tmpl_path):
        results.append((ERROR, name, "template not found"))
        return
    wb = xl2.load_workbook(tmpl_path)
    ws = wb.active
    ws.cell(cell_row, cell_col).value = bad_value
    buf = BytesIO(); wb.save(buf); buf.seek(0)
    xlsx_bytes = buf.getvalue()

    workdir = tempfile.mkdtemp(prefix="junc_test_")
    captured_msg = []
    def fake_msgbox(hwnd, text, caption, flags):
        captured_msg.append(text); return 1
    orig_dir = os.getcwd()
    try:
        with open(os.path.join(workdir, "volume_calculator.xlsx"), "wb") as f:
            f.write(xlsx_bytes)
        output_src = os.path.join(os.path.dirname(__file__), "OUTPUT.xlsx")
        if os.path.exists(output_src):
            shutil.copy2(output_src, os.path.join(workdir, "OUTPUT.xlsx"))
        os.chdir(workdir)
        devnull2 = io.StringIO()
        with patch.object(ctypes.windll.user32, 'MessageBoxW', fake_msgbox):
            try:
                import Phaser
                with contextlib.redirect_stdout(devnull2):
                    Phaser.main()
                msg = "(no error raised)"
                status = PASS if expected_contains is None else FAIL
            except SystemExit:
                msg = captured_msg[-1] if captured_msg else "(exit() no MessageBox)"
                status = PASS if (expected_contains and expected_contains in msg) else FAIL
            except ValueError as exc:
                msg = f"ValueError: {exc}"
                status = PASS if (expected_contains and expected_contains in str(exc)) else FAIL
            except Exception as exc:
                msg = f"Exception({type(exc).__name__}): {exc}"
                status = PASS if (expected_contains and expected_contains in str(exc)) else FAIL
    finally:
        os.chdir(orig_dir)
        shutil.rmtree(workdir, ignore_errors=True)
    results.append((status, name, msg))
    print(f"{status} | {name}")
    print(f"       msg: {msg}\n")

# Volume cell for NR morning = row 4, col 4
run_b6_raw_excel("B6 NR volume='hello' in Excel (non-numeric)",
    4, 4, "hello",
    expected_contains="numbers")

# B7: NR volume with no north right lane
# Build full volumes dict to avoid nested-update KeyError in helper
_vols_b7 = {
    "morning": {d: {"R": 0, "T": 0, "L": 0} for d in ["N","S","E","W"]},
    "evening": {d: {"R": 0, "T": 0, "L": 0} for d in ["N","S","E","W"]},
}
_vols_b7["morning"]["N"]["R"] = 300
_vols_b7["evening"]["N"]["R"] = 300
run_phaser_read("B7 NR=300 but no right lane in N",
    {"volumes": _vols_b7,
     "lanes": {"N": {"R": 0, "RT": 0, "T": 2, "TL": 0, "L": 1, "RTL": 0, "RL": 0}}},
    expected_contains="North right-turn volume")

# B8: Nataz invalid on N-RT lane
run_phaser_read("B8 N-RT nataz=5 (invalid >3)",
    {"nataz": {"N": {"RT": 5}},
     "lanes": {"N": {"RT": 1}}},
    expected_contains="nataz")

# B9: ERT=1 AND ETL=1 - actually valid (same as NRT+NTL), no error expected
run_phaser_read("B9 East ERT=1 and ETL=1 (two DIFFERENT complex types - valid)",
    {"lanes": {"E": {"RT": 1, "TL": 1}}})

# B9b: ERT=2 (single type > 1 - invalid)
run_phaser_read("B9b East ElanesRT=2 (invalid, single complex > 1)",
    {"lanes": {"E": {"RT": 2}}},
    expected_contains="East routing error")

# B10: All lanes zero, all volumes zero (trivial case)
run_phaser_read("B10 all zeros - trivial case", {})

# B11: Very high volumes with proper lanes
_vols_b11 = {p: {d: {"R": 500, "T": 5000, "L": 500} for d in ["N","S","E","W"]}
             for p in ["morning","evening"]}
_lanes_b11 = {d: {"R": 1, "RT": 0, "T": 2, "TL": 0, "L": 1, "RTL": 0, "RL": 0}
              for d in ["N","S","E","W"]}
run_phaser_read("B11 extreme volumes (5000 T, 500 R/L each dir)",
    {"volumes": _vols_b11, "lanes": _lanes_b11})

# B12: capacity=0 in instructions
run_phaser_read("B12 capacity=0 (may cause division by zero)",
    {"instructions": {"capacity": 0}})

# B13: NR volume with nataz blocking N-RT's R movement, only N-RT lane for R
_vols_b13 = {p: {d: {"R": 0, "T": 0, "L": 0} for d in ["N","S","E","W"]}
             for p in ["morning","evening"]}
_vols_b13["morning"]["N"]["R"] = 200
_vols_b13["evening"]["N"]["R"] = 200
run_phaser_read("B13 NR=200 only via N-RT, nataz=2 blocks R on RT -> missing north right",
    {"volumes": _vols_b13,
     "lanes": {"N": {"R": 0, "RT": 1, "T": 2, "TL": 0, "L": 1, "RTL": 0, "RL": 0}},
     "nataz": {"N": {"RT": 2}}},
    expected_contains="North right-turn volume")

# B14: Float lane value - note: create_excel does int(1.5)=1, so bypasses b_optimization check
# Test directly via raw Excel write to see if Phaser catches it
run_b6_raw_excel("B14 N-T lane = 1.5 in Excel (float - should catch as non-integer)",
    8, 5, 1.5,   # row 8, col 5 = N-T lane cell
    expected_contains="integer")

# B15: Negative lane count
run_phaser_read("B15 N-T lane = -1 (negative)",
    {"lanes": {"N": {"T": -1}}},
    expected_contains="Negative lane count")

# B16: inflation=0.0 (explicit float zero) -> should raise error
run_phaser_read("B16 inflation=0.0 (float zero - invalid)",
    {"instructions": {"inflation": 0.0}},
    expected_contains="Invalid inflation factor")

# B17: NL volume exists but all left-capable north lanes = 0
_vols_b17 = {p: {d: {"R": 0, "T": 0, "L": 0} for d in ["N","S","E","W"]}
             for p in ["morning","evening"]}
_vols_b17["morning"]["N"]["L"] = 200
_vols_b17["evening"]["N"]["L"] = 200
run_phaser_read("B17 NL=200 but all N-left lanes = 0",
    {"volumes": _vols_b17,
     "lanes": {"N": {"R": 1, "RT": 0, "T": 2, "TL": 0, "L": 0, "RTL": 0, "RL": 0}}},
    expected_contains="North left-turn volume")

# B18: East volumes but no east lanes
_vols_b18 = {p: {d: {"R": 0, "T": 0, "L": 0} for d in ["N","S","E","W"]}
             for p in ["morning","evening"]}
_vols_b18["morning"]["E"] = {"R": 100, "T": 300, "L": 100}
_vols_b18["evening"]["E"] = {"R": 100, "T": 300, "L": 100}
run_phaser_read("B18 East volumes exist but all east lanes = 0",
    {"volumes": _vols_b18,
     "lanes": {"E": {"R": 0, "RT": 0, "T": 0, "TL": 0, "L": 0, "RTL": 0, "RL": 0}}},
    expected_contains="East right-turn volume")

# ===============================================================================
# SUMMARY
# ===============================================================================
print("=" * 70)
print("SUMMARY")
print("=" * 70)

pass_count = sum(1 for r in results if r[0] == PASS)
fail_count = sum(1 for r in results if r[0] == FAIL)
error_count = sum(1 for r in results if r[0] == ERROR)

print(f"Total: {len(results)}  |  PASS: {pass_count}  |  FAIL (unexpected): {fail_count}  |  ERROR: {error_count}\n")

print("--- Cases where error message is missing or unclear ---")
for status, name, msg in results:
    if status != PASS or "no error" in msg:
        print(f"  {status} | {name}")
        print(f"         current msg: {msg}")
print()

print("--- All results ---")
for status, name, msg in results:
    print(f"  {status} | {name}")
    print(f"         -> {msg}")
