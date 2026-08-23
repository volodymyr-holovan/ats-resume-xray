"""Shared pipeline: file-type dispatch, extraction, and the rule engine,
used by both the CLI and the Streamlit app so this logic exists in exactly
one place instead of being duplicated across the two entry points.
"""

import io
import tempfile
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

from .docx_extract import extract_docx_full, extract_docx_naive
from .engine import Finding, run_rules
from .extract import extract_layout_aware, extract_naive
from .field_report import build_field_report
from .score import ScoreBreakdown, score_resume

SUPPORTED_SUFFIXES = (".pdf", ".docx")

MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024
"""50 MB. Far above any real resume — it exists to bound worst-case
processing time for untrusted uploads (the web app's actual threat
boundary), not because real files need the headroom. Raised from 10 MB so
image-heavy design-tool exports are not turned away."""

MAX_DOCX_UNCOMPRESSED_BYTES = 100 * 1024 * 1024
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
    score: ScoreBreakdown
    rendered_pages: list = field(default_factory=list)
    """Page images with findings boxed on them. Populated only when analysis
    is asked to render, and only for PDFs -- rendering costs real time, and
    a DOCX has no page geometry to draw on."""


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


def analyze_path(file_path: str, render: bool = False) -> AnalysisResult:
    """Extract text, run the rule engine, and score a file already on disk.

    Set ``render`` to also produce page images with findings boxed on them.
    It is off by default because rendering is the slowest step here and only
    the visual UI needs it.
    """
    naive_text, aware_text = extract_text(file_path)
    findings = run_rules(file_path, naive_text, aware_text)
    aware_fields = build_field_report(aware_text)
    naive_fields = build_field_report(naive_text)
    breakdown = score_resume(aware_fields, naive_fields, findings)

    rendered: list = []
    if render:
        suffix = Path(file_path).suffix.lower()
        if suffix == ".pdf":
            rendered = _render(file_path, findings)
        elif suffix == ".docx":
            findings, rendered = _render_docx(file_path, findings, aware_fields, naive_fields)

    return AnalysisResult(
        naive_text=naive_text,
        aware_text=aware_text,
        findings=findings,
        score=breakdown,
        rendered_pages=rendered,
    )


def _render(pdf_path: str, findings: list[Finding]) -> list:
    from .overlay import render_pages_with_findings

    return render_pages_with_findings(pdf_path, findings)


def _render_docx(
    docx_path: str,
    findings: list[Finding],
    aware_fields: dict,
    naive_fields: dict,
) -> tuple[list[Finding], list]:
    """Lay the DOCX out as pages and place its findings on them.

    Returns the findings unchanged and no pages when LibreOffice is not
    installed: without a layout engine there is no page to draw on, and
    guessing at one would put boxes on positions the reader's own word
    processor would not agree with.
    """
    from .docx_render import convert_docx_to_pdf
    from .engine import attach_docx_regions
    from .structure import analyze_structure

    with tempfile.TemporaryDirectory() as render_dir:
        converted = convert_docx_to_pdf(docx_path, render_dir)
        if converted is None:
            return findings, []

        located = attach_docx_regions(
            converted, findings, analyze_structure(docx_path), aware_fields, naive_fields
        )
        return located, _render(converted, located)


def analyze_bytes(file_bytes: bytes, filename: str, render: bool = False) -> AnalysisResult:
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
        return analyze_path(tmp_path, render=render)
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
