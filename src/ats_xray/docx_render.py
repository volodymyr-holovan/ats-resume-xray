"""Laying out a DOCX so it can be shown as pages.

A DOCX stores content and styling, not positions: there are no page
coordinates in the file until something applies the layout rules. So to show
a DOCX the way we show a PDF, we hand it to LibreOffice in headless mode,
which produces a PDF laid out the way a word processor would, and work from
that.

LibreOffice is an external program rather than a Python package, so it may
simply not be present. Every function here degrades to None instead of
raising, and callers fall back to the text-only view.
"""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

CONVERSION_TIMEOUT_SECONDS = 90

_WINDOWS_CANDIDATES = (
    r"D:\Programs\LibreOffice\program\soffice.exe",
    r"C:\Program Files\LibreOffice\program\soffice.exe",
    r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
)


def find_soffice() -> str | None:
    """Locate the LibreOffice binary, or return None if it is not installed.

    ``ATS_XRAY_SOFFICE`` overrides the search, for installs in unusual
    locations.
    """
    override = os.environ.get("ATS_XRAY_SOFFICE")
    if override and Path(override).exists():
        return override

    for name in ("soffice", "libreoffice"):
        found = shutil.which(name)
        if found:
            return found

    for candidate in _WINDOWS_CANDIDATES:
        if Path(candidate).exists():
            return candidate

    return None


def convert_docx_to_pdf(docx_path: str, out_dir: str) -> str | None:
    """Convert a DOCX to PDF and return the new file's path, or None if
    LibreOffice is unavailable or the conversion fails.

    Each call gets a throwaway LibreOffice user profile. Without one,
    concurrent conversions contend for the shared default profile and the
    second one silently produces nothing -- which matters here because a
    deployed app can be handling more than one upload at a time.
    """
    soffice = find_soffice()
    if soffice is None:
        return None

    source = Path(docx_path)

    with tempfile.TemporaryDirectory() as profile_dir:
        profile_url = Path(profile_dir).as_uri()
        try:
            subprocess.run(
                [
                    soffice,
                    f"-env:UserInstallation={profile_url}",
                    "--headless",
                    "--norestore",
                    "--convert-to",
                    "pdf",
                    "--outdir",
                    out_dir,
                    str(source),
                ],
                capture_output=True,
                timeout=CONVERSION_TIMEOUT_SECONDS,
                check=False,
            )
        except (subprocess.TimeoutExpired, OSError):
            return None

    # LibreOffice names the output after the input, ignoring --outdir for the
    # filename itself, and reports success on stdout even when it wrote
    # nothing -- so trust the file system rather than the return code.
    produced = Path(out_dir) / f"{source.stem}.pdf"
    return str(produced) if produced.exists() else None
