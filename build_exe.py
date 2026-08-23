"""Builds the single-file Windows executable.

Run with: python build_exe.py

Streamlit is awkward to freeze: it loads its own static assets and reads
package metadata at import time, neither of which PyInstaller finds by
following imports alone. ``--collect-all streamlit`` pulls both in. The
same applies to pdfplumber and python-docx, which ship data files.

The result is one .exe with no installer and no Python needed on the
target machine. LibreOffice is *not* bundled -- it is a separate program
of its own, so DOCX page previews fall back to the text-only view unless
the user has it installed. Everything else works offline.
"""

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
VERSION_FILE = ROOT / "build" / "version_info.txt"

APP_NAME = "ATS-Resume-X-Ray"
AUTHOR = "Volodymyr Holovan"
DESCRIPTION = "Shows what a resume-parsing pipeline actually extracts from your CV"


def read_version() -> str:
    text = (ROOT / "src" / "ats_xray" / "__init__.py").read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.startswith("__version__"):
            return line.split('"')[1]
    raise SystemExit("could not read __version__")


def write_version_info(version: str) -> Path:
    """Write the Windows VERSIONINFO resource.

    This is what fills in the Details tab of the file's properties and the
    publisher line some prompts show. It is *not* a signature: it does not
    prevent SmartScreen's "unknown publisher" warning or stop antivirus
    heuristics flagging a PyInstaller build. Only a paid code-signing
    certificate does that. It is still worth setting, so the file
    identifies itself honestly rather than appearing anonymous.
    """
    parts = version.split(".")
    while len(parts) < 4:
        parts.append("0")
    numeric = ", ".join(parts[:4])

    VERSION_FILE.parent.mkdir(parents=True, exist_ok=True)
    VERSION_FILE.write_text(
        f"""VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({numeric}),
    prodvers=({numeric}),
    mask=0x3f, flags=0x0, OS=0x40004, fileType=0x1, subtype=0x0, date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        '040904B0',
        [StringStruct('CompanyName', '{AUTHOR}'),
         StringStruct('FileDescription', '{DESCRIPTION}'),
         StringStruct('FileVersion', '{version}'),
         StringStruct('InternalName', '{APP_NAME}'),
         StringStruct('LegalCopyright', 'Copyright (c) 2026 {AUTHOR}. MIT License.'),
         StringStruct('OriginalFilename', '{APP_NAME}.exe'),
         StringStruct('ProductName', 'ATS Resume X-Ray'),
         StringStruct('ProductVersion', '{version}')])
    ]),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
""",
        encoding="utf-8",
    )
    return VERSION_FILE


def build() -> Path:
    version = read_version()
    version_info = write_version_info(version)

    separator = ";" if sys.platform == "win32" else ":"
    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--name",
        APP_NAME,
        "--icon",
        str(ROOT / "assets" / "icon.ico"),
        "--version-file",
        str(version_info),
        # app.py and the package are executed by Streamlit as data, not
        # imported by the launcher, so they have to be added explicitly.
        "--add-data",
        f"{ROOT / 'app.py'}{separator}.",
        "--add-data",
        f"{ROOT / 'src' / 'ats_xray'}{separator}ats_xray",
        "--add-data",
        f"{ROOT / '.streamlit'}{separator}.streamlit",
        "--add-data",
        f"{ROOT / 'assets'}{separator}assets",
        # These three ship data files and read their own metadata, which
        # import-following alone does not pick up.
        "--collect-all",
        "streamlit",
        "--collect-all",
        "pdfplumber",
        "--collect-all",
        "docx",
        "--hidden-import",
        "ats_xray",
        str(ROOT / "desktop.py"),
    ]

    print("Building", APP_NAME, version)
    subprocess.run(command, check=True)

    produced = DIST / f"{APP_NAME}.exe"
    if not produced.exists():
        raise SystemExit("build reported success but produced no .exe")

    size_mb = produced.stat().st_size / (1024 * 1024)
    print(f"\nBuilt {produced} ({size_mb:.0f} MB)")
    return produced


if __name__ == "__main__":
    if shutil.which("pyinstaller") is None:
        print("PyInstaller not found on PATH; using the current interpreter's module instead.")
    build()
