"""Locating a section on a PDF page.

Findings that come from comparing *text* (a section that survives
layout-aware reading but vanishes under naive reading) have no coordinates
of their own, because the comparison happens after extraction. To point at
them on the page, we go back to the PDF and find where that section sits.

A section is its heading plus everything under it, so the box covers the
content actually at risk rather than just the words of the heading.
"""

import pdfplumber

from ._pdf_words import DEFAULT_LINE_TOLERANCE, group_words_into_lines
from .extract import _cluster_columns
from .regions import Region
from .sections import SECTION_ALIASES, normalize_heading

ALL_HEADING_ALIASES = {alias for aliases in SECTION_ALIASES.values() for alias in aliases}


def find_section_regions(
    pdf_path: str,
    target_aliases: set[str],
    line_tolerance: float = DEFAULT_LINE_TOLERANCE,
) -> list[Region]:
    """Return one region per section whose heading matches ``target_aliases``,
    spanning the heading and the lines beneath it.

    A section ends at the next recognized heading *of any kind* in the same
    column, or at the end of that column. Lines are grouped per column rather
    than across the page, so a section in a narrow sidebar is measured within
    its own column instead of swallowing whatever sits beside it.
    """
    regions: list[Region] = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            for column_words in _cluster_columns(page.extract_words()):
                lines = group_words_into_lines(column_words, line_tolerance)
                heading_indices = [
                    i for i, line in enumerate(lines) if normalize_heading(line["text"]) in ALL_HEADING_ALIASES
                ]

                for position, start in enumerate(heading_indices):
                    if normalize_heading(lines[start]["text"]) not in target_aliases:
                        continue
                    end = heading_indices[position + 1] if position + 1 < len(heading_indices) else len(lines)
                    regions.append(_span(page_number, lines[start:end]))

    return regions


def _span(page_number: int, lines: list[dict]) -> Region:
    return Region(
        page=page_number,
        x0=min(line["x0"] for line in lines),
        top=min(line["top"] for line in lines),
        x1=max(line["x1"] for line in lines),
        bottom=max(line["bottom"] for line in lines),
    )
