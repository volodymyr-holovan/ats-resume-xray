"""Locating things on a PDF page: text lines matching a predicate, and the
column blocks a page is split into.

Findings that come from comparing *text* (a section heading that survives
layout-aware reading but vanishes under naive reading) have no coordinates
of their own, because the comparison happens after extraction. To point at
them on the page, we go back to the PDF and find where that text sits.
"""

from typing import Callable

import pdfplumber

from ._pdf_words import DEFAULT_LINE_TOLERANCE, group_words_into_lines
from .extract import DEFAULT_MIN_COLUMN_GAP, _cluster_columns
from .regions import Region, region_from_words


def find_line_regions(
    pdf_path: str,
    matches: Callable[[str], bool],
    line_tolerance: float = DEFAULT_LINE_TOLERANCE,
) -> list[Region]:
    """Return a region for every text line whose text satisfies ``matches``.

    Lines are built per column, not across the full page width, so a heading
    in a narrow sidebar produces a box around the heading itself rather than
    one spanning everything at that height.
    """
    regions: list[Region] = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            for column_words in _cluster_columns(page.extract_words()):
                for line in group_words_into_lines(column_words, line_tolerance):
                    if matches(line["text"]):
                        region = region_from_words(page_number, line["words"])
                        if region:
                            regions.append(region)

    return regions


def find_column_regions(pdf_path: str, min_gap: float = DEFAULT_MIN_COLUMN_GAP) -> list[Region]:
    """Return one region per column, for pages that split into two or more.

    Single-column pages produce nothing: there is no column boundary to show
    and outlining the whole page would be noise.
    """
    regions: list[Region] = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            columns = _cluster_columns(page.extract_words(), min_gap=min_gap)
            if len(columns) < 2:
                continue
            for column_words in columns:
                region = region_from_words(page_number, column_words)
                if region:
                    regions.append(region)

    return regions
