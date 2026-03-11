"""
font_installer.py — Install fonts required by JUNC.

Installs to the current user's font directory (no admin required on Windows 10+).
Can be run directly:  python font_installer.py

Fonts needed:
  - Traffic Arrows 2 Med normal  (bundled in fonts/TrafficArrows.ttf)
  - Assistant                    (Google Font — downloaded automatically if missing)
"""

import ctypes
import os
import shutil
import struct
import winreg
from pathlib import Path
from urllib import request

_SRC_DIR = Path(__file__).parent
FONTS_PROJECT_DIR = _SRC_DIR / "fonts"

# User-level fonts directory — no admin needed on Windows 10+
USER_FONTS_DIR = Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "Windows" / "Fonts"
SYSTEM_FONTS_DIR = Path(os.environ.get("SystemRoot", r"C:\Windows")) / "Fonts"

# Registry key for per-user font registration
_REG_KEY = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"

# Assistant Variable Font — Google Fonts GitHub (OFL licensed, free to bundle/download)
ASSISTANT_URL = (
    "https://github.com/google/fonts/raw/main/ofl/assistant/"
    "Assistant%5Bwght%5D.ttf"
)
ASSISTANT_FILENAME = "Assistant-Variable.ttf"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _read_ttf_family_name(path: Path) -> str:
    """Return the internal family name (nameID=1) from a TTF file."""
    try:
        data = path.read_bytes()
        num_tables = struct.unpack(">H", data[4:6])[0]
        for i in range(num_tables):
            tag = data[12 + i * 16: 12 + i * 16 + 4].decode("ascii", "ignore")
            if tag == "name":
                tbl = struct.unpack(">I", data[12 + i * 16 + 8: 12 + i * 16 + 12])[0]
                count = struct.unpack(">H", data[tbl + 2: tbl + 4])[0]
                soff = struct.unpack(">H", data[tbl + 4: tbl + 6])[0]
                for j in range(count):
                    base = tbl + 6 + j * 12
                    name_id = struct.unpack(">H", data[base + 6: base + 8])[0]
                    length = struct.unpack(">H", data[base + 8: base + 10])[0]
                    offset = struct.unpack(">H", data[base + 10: base + 12])[0]
                    if name_id == 1:
                        raw = data[tbl + soff + offset: tbl + soff + offset + length]
                        try:
                            return raw.decode("utf-16-be").strip()
                        except Exception:
                            return raw.decode("latin-1", "ignore").strip()
    except Exception:
        pass
    return path.stem


def _font_installed(family_name: str) -> bool:
    """Check whether a font family is registered in the system or user registry."""
    for hive in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
        try:
            with winreg.OpenKey(hive, _REG_KEY) as key:
                i = 0
                while True:
                    try:
                        reg_name, _, _ = winreg.EnumValue(key, i)
                        if family_name.lower() in reg_name.lower():
                            return True
                        i += 1
                    except OSError:
                        break
        except OSError:
            pass
    # Also check for the file in the known font directories
    for font_dir in (USER_FONTS_DIR, SYSTEM_FONTS_DIR):
        for f in font_dir.glob("*.ttf"):
            if family_name.lower().replace(" ", "") in f.stem.lower().replace(" ", ""):
                return True
    return False


def _install_one(ttf_path: Path) -> tuple[bool, str]:
    """Copy one TTF file into the user fonts dir and register it."""
    try:
        USER_FONTS_DIR.mkdir(parents=True, exist_ok=True)
        dst = USER_FONTS_DIR / ttf_path.name
        shutil.copy2(ttf_path, dst)
        family = _read_ttf_family_name(ttf_path)
        # Register in HKCU (no admin needed)
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, _REG_KEY, 0, winreg.KEY_SET_VALUE
        ) as key:
            winreg.SetValueEx(key, f"{family} (TrueType)", 0, winreg.REG_SZ, str(dst))
        # Load into current Windows session
        ctypes.windll.gdi32.AddFontResourceExW(str(dst), 0, 0)
        return True, ""
    except Exception as exc:
        return False, str(exc)


def _broadcast_font_change():
    HWND_BROADCAST = 0xFFFF
    WM_FONTCHANGE = 0x001D
    ctypes.windll.user32.SendMessageW(HWND_BROADCAST, WM_FONTCHANGE, 0, 0)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_status() -> dict[str, bool]:
    """
    Return installation status for each required font.
    Keys are human-readable font family names, values are True/False.
    """
    status = {}
    # Fonts bundled in fonts/
    for f in sorted(FONTS_PROJECT_DIR.glob("*.ttf")):
        name = _read_ttf_family_name(f)
        status[name] = _font_installed(name)
    # Assistant (may not be in fonts/ yet)
    status["Assistant"] = _font_installed("Assistant")
    return status


def install_fonts(download_assistant: bool = True) -> list[tuple[str, bool, str]]:
    """
    Install all missing fonts.

    Parameters
    ----------
    download_assistant : bool
        If True and Assistant is not found locally, download it from Google Fonts.

    Returns
    -------
    list of (font_name, success, error_message)
    """
    results = []

    # 1. Install bundled fonts from fonts/ dir
    for ttf in sorted(FONTS_PROJECT_DIR.glob("*.ttf")):
        name = _read_ttf_family_name(ttf)
        if _font_installed(name):
            results.append((name, True, "already installed"))
            continue
        ok, err = _install_one(ttf)
        results.append((name, ok, err))

    # 2. Handle Assistant
    if not _font_installed("Assistant"):
        assistant_local = FONTS_PROJECT_DIR / ASSISTANT_FILENAME
        if not assistant_local.exists() and download_assistant:
            try:
                request.urlretrieve(ASSISTANT_URL, assistant_local)
            except Exception as exc:
                results.append(("Assistant", False, f"download failed: {exc}"))
                assistant_local = None
        if assistant_local and assistant_local.exists():
            ok, err = _install_one(assistant_local)
            results.append(("Assistant", ok, err))
    else:
        results.append(("Assistant", True, "already installed"))

    _broadcast_font_change()
    return results


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")

    print("JUNC Font Installer")
    print("===================")
    print("\nChecking font status...")
    for font, installed in get_status().items():
        mark = "OK" if installed else "--"
        print(f"  [{mark}]  {font}")

    print("\nInstalling missing fonts...")
    for name, ok, msg in install_fonts():
        if ok:
            print(f"  [OK]  {name}  ({msg})")
        else:
            print(f"  [!!]  {name}  -- {msg}")

    print("\nDone. Restart PowerPoint if it was open.")
