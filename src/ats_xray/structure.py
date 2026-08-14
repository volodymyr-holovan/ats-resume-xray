"""Unified structural analysis: runs every Day 2 detector applicable to a
file's type and returns their findings in one place.
"""

from pathlib import Path

from .docx_structure import extract_docx_headers_footers, find_docx_text_box_content
from .pdf_fonts import find_non_embedded_fonts
from .pdf_headers_footers import find_repeated_header_footer_lines
from .pdf_images import find_large_textless_images


def analyze_structure(file_path: str) -> dict:
    """Run every structural detector for the file's type and return a dict
    of findings.

    PDF keys: ``non_embedded_fonts``, ``repeated_header_footer_lines``,
    ``textless_images``.

    DOCX keys: ``headers_footers``, ``text_box_content``.
    """
    suffix = Path(file_path).suffix.lower()

    if suffix == ".pdf":
        return {
            "non_embedded_fonts": find_non_embedded_fonts(file_path),
            "repeated_header_footer_lines": find_repeated_header_footer_lines(file_path),
            "textless_images": find_large_textless_images(file_path),
        }

    if suffix == ".docx":
        return {
            "headers_footers": extract_docx_headers_footers(file_path),
            "text_box_content": find_docx_text_box_content(file_path),
        }

    raise ValueError(f"Unsupported file type: {suffix or '(none)'}. Use .pdf or .docx.")
