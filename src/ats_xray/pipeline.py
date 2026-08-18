"""Shared pipeline: file-type dispatch, extraction, and the rule engine,
used by both the CLI and the Streamlit app so this logic exists in exactly
one place instead of being duplicated across the two entry points.
"""

import tempfile
from dataclasses import dataclass
from pathlib import Path

from .docx_extract import extract_docx_full, extract_docx_naive
from .engine import Finding, run_rules
from .extract import extract_layout_aware, extract_naive

SUPPORTED_SUFFIXES = (".pdf", ".docx")


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
    """
    suffix = Path(filename).suffix.lower()
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp_file:
        tmp_file.write(file_bytes)
        tmp_path = tmp_file.name

    try:
        return analyze_path(tmp_path)
    finally:
        Path(tmp_path).unlink(missing_ok=True)
