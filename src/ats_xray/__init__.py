"""Public API surface: the functions most callers need, re-exported from
their implementing modules. Internals (detectors, the rule registry) are
still importable directly from their own modules for anyone who wants
finer-grained access.
"""

__version__ = "0.3.0"
"""Kept here rather than only in pyproject.toml so a frozen build, which has
no package metadata to read, can still tell the update check what it is."""

from .extract import extract_layout_aware, extract_naive
from .docx_extract import extract_docx_full, extract_docx_naive
from .structure import analyze_structure
from .field_report import build_field_report
from .engine import run_rules
from .pipeline import analyze_bytes, analyze_path

__all__ = [
    "extract_naive",
    "extract_layout_aware",
    "extract_docx_naive",
    "extract_docx_full",
    "analyze_structure",
    "build_field_report",
    "run_rules",
    "analyze_path",
    "analyze_bytes",
]
