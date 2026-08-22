"""Detects header/footer lines: text that repeats, verbatim aside from
changing digits (e.g. page numbers), in the same top/bottom page zone
across multiple pages of a PDF.

Why this matters: many resume-parsing pipelines treat repeated
header/footer content as boilerplate and strip it before extracting the
"real" content. That is usually the right call for page numbers — but it
becomes a problem if a candidate has put essential information (a phone
number, an email) inside a running header or footer, since that content
risks being silently discarded along with the boilerplate.

Detecting a repetition needs at least two pages, so this is a no-op on
single-page resumes.
"""

import re

import pdfplumber

from ._pdf_words import DEFAULT_LINE_TOLERANCE, group_words_into_lines
from .regions import Region

DEFAULT_ZONE_FRACTION = 0.12

_DIGIT_RUN = re.compile(r"\d+")


def find_repeated_header_footer_lines(
    pdf_path: str,
    zone_fraction: float = DEFAULT_ZONE_FRACTION,
    line_tolerance: float = DEFAULT_LINE_TOLERANCE,
) -> list[dict]:
    """Return repeated header/footer lines as
    ``[{"zone": "header"|"footer", "text": str, "pages": [1, 2, ...],
    "regions": [Region, ...]}, ...]``, in first-seen order. Page numbers are
    1-indexed, and each region locates one occurrence on its page.
    """
    header_occurrences: dict[str, dict] = {}
    footer_occurrences: dict[str, dict] = {}

    with pdfplumber.open(pdf_path) as pdf:
        if len(pdf.pages) < 2:
            return []

        for page_number, page in enumerate(pdf.pages, start=1):
            lines = group_words_into_lines(page.extract_words(), line_tolerance)
            header_limit = page.height * zone_fraction
            footer_limit = page.height * (1 - zone_fraction)

            for line in lines:
                normalized = _normalize(line["text"])
                if not normalized:
                    continue
                if line["bottom"] <= header_limit:
                    _record(header_occurrences, normalized, line, page_number)
                elif line["top"] >= footer_limit:
                    _record(footer_occurrences, normalized, line, page_number)

    findings = []
    for zone, occurrences in (("header", header_occurrences), ("footer", footer_occurrences)):
        for entry in occurrences.values():
            if len(entry["pages"]) >= 2:
                findings.append(
                    {
                        "zone": zone,
                        "text": entry["sample_text"],
                        "pages": entry["pages"],
                        "regions": entry["regions"],
                    }
                )
    return findings


def _record(occurrences: dict, normalized: str, line: dict, page_number: int) -> None:
    entry = occurrences.setdefault(normalized, {"sample_text": line["text"], "pages": [], "regions": []})
    entry["pages"].append(page_number)
    entry["regions"].append(
        Region(page=page_number, x0=line["x0"], top=line["top"], x1=line["x1"], bottom=line["bottom"])
    )


def _normalize(text: str) -> str:
    """Collapse digit runs so "Page 1 of 3" and "Page 2 of 3" are treated as
    the same repeated pattern, and normalize whitespace/case for comparison.
    """
    return _DIGIT_RUN.sub("#", text).strip().lower()
