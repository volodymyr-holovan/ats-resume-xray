"""Shared pipeline: file-type dispatch, extraction, and the rule engine,
used by both the CLI and the Streamlit app so this logic exists in exactly
one place instead of being duplicated across the two entry points.
"""

import io
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path

from .docx_extract import extract_docx_full, extract_docx_naive
from .engine import Finding, run_rules
from .extract import extract_layout_aware, extract_naive

SUPPORTED_SUFFIXES = (".pdf", ".docx")

MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024
"""10 MB. No legitimate resume — even a DOCX with a photo — comes close to
this; it exists to bound worst-case processing time for untrusted uploads
(the web app's actual threat boundary), not because real files need it."""

MAX_DOCX_UNCOMPRESSED_BYTES = 20 * 1024 * 1024
"""A DOCX is a zip archive, so a small upload can still decompress to a
huge amount of content ("zip bomb"). Zip central-directory metadata
records each entry's uncompressed size and is cheap to read without
actually inflating anything, so we check it before python-docx (or
anything downstream) ever does."""


@dataclass(frozen=True)
class AnalysisResult:
    naive_text: str
    aware_text: str
    findings: list[Finding]


def extract_text(file_path: str) -> tuple[str, str]:
    """Return (naive_text, aware_text) for a PDF or DOCX file already on
    disk. Raises ValueError for any other extension.
    """
    suffix = Path(file_path).suffix.lower()
    if suffix == ".pdf":
        return extract_naive(file_path), extract_layout_aware(file_path)
    if suffix == ".docx":
        return extract_docx_naive(file_path), extract_docx_full(file_path)
    raise ValueError(f"Unsupported file type: {suffix or '(none)'}. Use .pdf or .docx.")


def analyze_path(file_path: str) -> AnalysisResult:
    """Extract text and run the rule engine against a file already on disk."""
    naive_text, aware_text = extract_text(file_path)
    findings = run_rules(file_path, naive_text, aware_text)
    return AnalysisResult(naive_text=naive_text, aware_text=aware_text, findings=findings)


def analyze_bytes(file_bytes: bytes, filename: str) -> AnalysisResult:
    """Write file_bytes to a temporary file (named to match filename's
    extension, so format detection works), analyze it, then delete the
    temp file — regardless of whether analysis succeeded.

    This is the entry point for untrusted input (the web app's file
    uploader), so it rejects oversized or implausible files before any
    real parsing work happens.
    """
    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise ValueError(
            f"File is {len(file_bytes) / (1024 * 1024):.1f} MB, over the "
            f"{MAX_FILE_SIZE_BYTES // (1024 * 1024)} MB limit for a resume upload."
        )

    suffix = Path(filename).suffix.lower()
    if suffix == ".docx":
        _reject_docx_zip_bomb(file_bytes)

    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp_file:
        tmp_file.write(file_bytes)
        tmp_path = tmp_file.name

    try:
        return analyze_path(tmp_path)
    finally:
        Path(tmp_path).unlink(missing_ok=True)


def _reject_docx_zip_bomb(file_bytes: bytes) -> None:
    """Raise ValueError if the DOCX's declared uncompressed size is
    implausible for a resume. A corrupt/non-zip file is left for the real
    parser to raise a clearer error on, rather than rejected here.
    """
    try:
        with zipfile.ZipFile(io.BytesIO(file_bytes)) as archive:
            total_uncompressed = sum(entry.file_size for entry in archive.infolist())
    except zipfile.BadZipFile:
        return

    if total_uncompressed > MAX_DOCX_UNCOMPRESSED_BYTES:
        raise ValueError(
            f"This DOCX claims to contain {total_uncompressed / (1024 * 1024):.0f} MB "
            "of uncompressed content, which isn't plausible for a resume. Rejected "
            "before processing."
        )
