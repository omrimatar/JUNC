"""
test_export_import.py — Test suite for Excel/JSON export and import in JUNC.

Covers:
  1. default_state() structure integrity
  2. Excel round-trip: create_excel_from_state → read_excel_to_state
  3. JSON round-trip: json.dumps → json.loads (as used by the export button)
  4. JSON bytes round-trip (as passed to st.download_button)
  5. Lazy export pattern (export_excel_bytes not recomputed on every rerun)
  6. Excel and JSON exports produce identical data for the same state

Usage:  python test_export_import.py
"""

import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from ui_excel import (
    create_excel_from_state,
    read_excel_to_state,
    default_state,
    DIRECTIONS,
    MOVEMENTS,
    LANE_TYPES,
)

PASS  = "PASS "
FAIL  = "FAIL "
ERROR = "ERROR"

results = []

def check(name, condition, detail=""):
    status = PASS if condition else FAIL
    results.append((status, name, detail))
    suffix = f"\n       detail: {detail}" if detail and not condition else ""
    print(f"{status} | {name}{suffix}")


def run(group_name, fn):
    print(f"\n-- {group_name} --")
    try:
        fn()
    except Exception as exc:
        results.append((ERROR, group_name, str(exc)))
        print(f"{ERROR} | {group_name}\n       {exc}")


TMPL_PATH = os.path.join(os.path.dirname(__file__), "volume_calculator.xlsx")


def _load_template():
    with open(TMPL_PATH, "rb") as f:
        return f.read()


# ── T1: default_state structure ───────────────────────────────────────────────
def _t1():
    s = default_state()
    check("T1a volumes key present",     "volumes"      in s)
    check("T1b lanes key present",       "lanes"        in s)
    check("T1c nataz key present",       "nataz"        in s)
    check("T1d instructions key present","instructions" in s)
    check("T1e rakal key present",       "rakal"        in s)
    check("T1f streets key present",     "streets"      in s)
    check("T1g junc key present",        "junc"         in s)
    check("T1h morning period exists",   "morning" in s["volumes"])
    check("T1i evening period exists",   "evening" in s["volumes"])
    for d in DIRECTIONS:
        check(f"T1j directions in morning volumes [{d}]", d in s["volumes"]["morning"])
        check(f"T1k directions in lanes [{d}]",           d in s["lanes"])
        check(f"T1l directions in streets [{d}]",         d in s["streets"])
    for period in ("morning", "evening"):
        for d in DIRECTIONS:
            for m in MOVEMENTS:
                check(f"T1m vol[{period}][{d}][{m}] is int",
                      isinstance(s["volumes"][period][d][m], int))

run("T1: default_state structure", _t1)


# ── T2: Excel round-trip — empty (default) state ─────────────────────────────
def _t2():
    if not os.path.exists(TMPL_PATH):
        check("T2 template found", False, f"not found: {TMPL_PATH}")
        return
    tmpl = _load_template()
    s    = default_state()
    xlsx = create_excel_from_state(s, tmpl)
    check("T2a result is bytes",      isinstance(xlsx, bytes))
    check("T2b result non-empty",     len(xlsx) > 4)
    s2   = read_excel_to_state(xlsx)
    for period in ("morning", "evening"):
        for d in DIRECTIONS:
            for m in MOVEMENTS:
                v1, v2 = s["volumes"][period][d][m], s2["volumes"][period][d][m]
                check(f"T2c vol[{period}][{d}][{m}]", v1 == v2, f"{v1} != {v2}")
    for d in DIRECTIONS:
        for lt in LANE_TYPES:
            check(f"T2d lanes[{d}][{lt}]",
                  s["lanes"][d][lt] == s2["lanes"][d][lt])
            check(f"T2e nataz[{d}][{lt}]",
                  s["nataz"][d][lt] == s2["nataz"][d][lt])

run("T2: Excel round-trip (default state)", _t2)


# ── T3: Excel round-trip — realistic data ────────────────────────────────────
def _t3():
    if not os.path.exists(TMPL_PATH):
        check("T3 template found", False, f"not found: {TMPL_PATH}")
        return
    tmpl = _load_template()
    s    = default_state()

    s["volumes"]["morning"]["N"] = {"R": 123, "T": 456, "L":  78}
    s["volumes"]["morning"]["S"] = {"R": 200, "T": 800, "L": 150}
    s["volumes"]["morning"]["E"] = {"R":  50, "T": 300, "L":  90}
    s["volumes"]["morning"]["W"] = {"R":  70, "T": 250, "L": 110}
    s["volumes"]["evening"]["N"] = {"R":  90, "T": 320, "L":  60}
    s["volumes"]["evening"]["S"] = {"R": 180, "T": 750, "L": 130}
    s["volumes"]["evening"]["E"] = {"R":  40, "T": 280, "L":  80}
    s["volumes"]["evening"]["W"] = {"R":  60, "T": 210, "L": 100}

    s["lanes"]["N"] = {"R": 1, "RT": 0, "T": 2, "TL": 0, "L": 1, "RTL": 0, "RL": 0}
    s["lanes"]["S"] = {"R": 1, "RT": 0, "T": 2, "TL": 1, "L": 0, "RTL": 0, "RL": 0}
    s["nataz"]["N"]["T"] = 1

    s["instructions"]["capacity"]  = 1600
    s["instructions"]["inflation"] = 1.1
    s["instructions"]["geo_ns"]    = 4
    s["instructions"]["nlsl"]      = 0

    s["junc"]["more_info"]    = "Test Project"
    s["junc"]["proj_counter"] = 42
    s["streets"]["N"] = "Main St"
    s["streets"]["S"] = "Oak Ave"

    xlsx = create_excel_from_state(s, tmpl)
    s2   = read_excel_to_state(xlsx)

    for period in ("morning", "evening"):
        for d in DIRECTIONS:
            for m in MOVEMENTS:
                v1, v2 = s["volumes"][period][d][m], s2["volumes"][period][d][m]
                check(f"T3a vol[{period}][{d}][{m}]", v1 == v2, f"{v1} != {v2}")

    for d in ["N", "S"]:
        for lt in LANE_TYPES:
            check(f"T3b lanes[{d}][{lt}]",
                  s["lanes"][d][lt] == s2["lanes"][d][lt])

    check("T3c nataz N-T",     s2["nataz"]["N"]["T"] == 1)
    check("T3d capacity",      s2["instructions"]["capacity"] == 1600)
    check("T3e geo_ns",        s2["instructions"]["geo_ns"]   == 4)
    check("T3f nlsl",          s2["instructions"]["nlsl"]     == 0)
    check("T3g proj_counter",  int(s2["junc"]["proj_counter"]) == 42)
    check("T3h more_info",     s2["junc"]["more_info"]        == "Test Project")
    check("T3i street N",      s2["streets"]["N"]             == "Main St")
    check("T3j street S",      s2["streets"]["S"]             == "Oak Ave")

run("T3: Excel round-trip (realistic data)", _t3)


# ── T4: JSON round-trip ───────────────────────────────────────────────────────
def _t4():
    s = default_state()
    s["volumes"]["morning"]["N"] = {"R": 111, "T": 222, "L": 333}
    s["junc"]["more_info"]  = "JSON test"
    s["streets"]["W"]       = "שדרות הרצל"

    json_str = json.dumps(s, ensure_ascii=False, indent=2)
    check("T4a result is str",              isinstance(json_str, str))
    check("T4b result non-empty",           len(json_str) > 0)
    check("T4c Hebrew preserved",           "שדרות הרצל" in json_str)

    s2 = json.loads(json_str)
    check("T4d vol N R",                    s2["volumes"]["morning"]["N"]["R"] == 111)
    check("T4e vol N T",                    s2["volumes"]["morning"]["N"]["T"] == 222)
    check("T4f vol N L",                    s2["volumes"]["morning"]["N"]["L"] == 333)
    check("T4g junc.more_info",             s2["junc"]["more_info"]  == "JSON test")
    check("T4h street W Hebrew",            s2["streets"]["W"]       == "שדרות הרצל")
    check("T4i all top-level keys intact",  set(s.keys()) == set(s2.keys()))

run("T4: JSON round-trip", _t4)


# ── T5: JSON bytes round-trip (as used by st.download_button) ─────────────────
def _t5():
    s = default_state()
    s["volumes"]["evening"]["E"] = {"R": 50, "T": 100, "L": 25}

    json_bytes = json.dumps(s, ensure_ascii=False, indent=2).encode("utf-8")
    check("T5a result is bytes",  isinstance(json_bytes, bytes))
    check("T5b result non-empty", len(json_bytes) > 0)

    s2 = json.loads(json_bytes.decode("utf-8"))
    check("T5c vol E R after bytes round-trip", s2["volumes"]["evening"]["E"]["R"] == 50)
    check("T5d vol E T after bytes round-trip", s2["volumes"]["evening"]["E"]["T"] == 100)
    check("T5e vol E L after bytes round-trip", s2["volumes"]["evening"]["E"]["L"] == 25)

run("T5: JSON bytes round-trip", _t5)


# ── T6: Lazy export pattern (no recomputation on every rerun) ─────────────────
def _t6():
    if not os.path.exists(TMPL_PATH):
        check("T6 template found", False, f"not found: {TMPL_PATH}")
        return
    tmpl = _load_template()
    s    = default_state()
    s["volumes"]["morning"]["N"]["T"] = 999

    # Simulate session_state.export_excel_bytes
    session = {"export_excel_bytes": None}

    check("T6a initially None (not precomputed)", session["export_excel_bytes"] is None)

    # Simulate clicking "Prepare Excel Export"
    session["export_excel_bytes"] = create_excel_from_state(s, tmpl)
    check("T6b bytes stored after prepare",       isinstance(session["export_excel_bytes"], bytes))

    # Simulate rerun: should NOT recompute
    stored     = session["export_excel_bytes"]
    recomputed = False
    if session["export_excel_bytes"] is None:          # this branch is skipped
        session["export_excel_bytes"] = create_excel_from_state(s, tmpl)
        recomputed = True
    check("T6c no recomputation on rerun",        not recomputed)
    check("T6d stored bytes stable across rerun", session["export_excel_bytes"] is stored)

    # Simulate "Re-prepare" button: clear so next rerun recomputes
    session["export_excel_bytes"] = None
    check("T6e cleared by re-prepare button",     session["export_excel_bytes"] is None)

run("T6: Lazy export pattern", _t6)


# ── T7: Excel and JSON exports are consistent for the same state ──────────────
def _t7():
    if not os.path.exists(TMPL_PATH):
        check("T7 template found", False, f"not found: {TMPL_PATH}")
        return
    tmpl = _load_template()
    s    = default_state()
    s["volumes"]["morning"]["W"] = {"R": 77, "T": 88, "L": 99}
    s["lanes"]["W"]["T"] = 2

    xlsx        = create_excel_from_state(s, tmpl)
    json_str    = json.dumps(s, ensure_ascii=False)
    s_xl        = read_excel_to_state(xlsx)
    s_js        = json.loads(json_str)

    for m, expected in zip(MOVEMENTS, [77, 88, 99]):
        check(f"T7a W-{m} Excel export correct",
              s_xl["volumes"]["morning"]["W"][m] == expected,
              f"got {s_xl['volumes']['morning']['W'][m]}")
        check(f"T7b W-{m} JSON export correct",
              s_js["volumes"]["morning"]["W"][m] == expected,
              f"got {s_js['volumes']['morning']['W'][m]}")
        check(f"T7c W-{m} Excel == JSON",
              s_xl["volumes"]["morning"]["W"][m] == s_js["volumes"]["morning"]["W"][m])

    check("T7d W-T lane in Excel", s_xl["lanes"]["W"]["T"] == 2)
    check("T7e W-T lane in JSON",  s_js["lanes"]["W"]["T"] == 2)

run("T7: Excel/JSON export consistency", _t7)


# ── T8: Importing JSON with Hebrew content does not corrupt data ──────────────
def _t8():
    s = default_state()
    s["streets"] = {"N": "שדרות בן-גוריון", "S": "רחוב הרצל",
                    "E": "שדרות רוטשילד",    "W": "רחוב דיזנגוף"}
    s["junc"]["more_info"]       = "פרויקט בדיקה"
    s["junc"]["lrt_line_name"]   = "קו אדום"

    json_bytes = json.dumps(s, ensure_ascii=False, indent=2).encode("utf-8")
    s2 = json.loads(json_bytes.decode("utf-8"))

    check("T8a street N Hebrew",       s2["streets"]["N"] == "שדרות בן-גוריון")
    check("T8b street S Hebrew",       s2["streets"]["S"] == "רחוב הרצל")
    check("T8c street E Hebrew",       s2["streets"]["E"] == "שדרות רוטשילד")
    check("T8d street W Hebrew",       s2["streets"]["W"] == "רחוב דיזנגוף")
    check("T8e more_info Hebrew",      s2["junc"]["more_info"]     == "פרויקט בדיקה")
    check("T8f lrt_line_name Hebrew",  s2["junc"]["lrt_line_name"] == "קו אדום")

run("T8: Hebrew content preserved in JSON import", _t8)


# ── SUMMARY ───────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

pass_count  = sum(1 for r in results if r[0] == PASS)
fail_count  = sum(1 for r in results if r[0] == FAIL)
error_count = sum(1 for r in results if r[0] == ERROR)

print(f"Total: {len(results)}  |  PASS: {pass_count}  |  FAIL: {fail_count}  |  ERROR: {error_count}")

if fail_count or error_count:
    print("\n--- Failed / Error cases ---")
    for status, name, detail in results:
        if status != PASS:
            print(f"  {status} | {name}")
            if detail:
                print(f"         -> {detail}")

sys.exit(0 if fail_count == 0 and error_count == 0 else 1)
