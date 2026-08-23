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


def find_text_regions(
    pdf_path: str,
    snippets: list[str],
    line_tolerance: float = DEFAULT_LINE_TOLERANCE,
) -> list[Region]:
    """Return a region for every line that carries any of ``snippets``.

    Used to place DOCX findings once the document has been laid out: the
    detectors work on XML and report the text they found, so the only way
    back to a position on the page is to look the text up again.

    Matching is loose on purpose. A word processor rewraps text, so a
    snippet extracted from a table cell or a text box may be split across
    lines by the time it is rendered -- a line counts as a match if it
    shares a long-enough run of words with the snippet, rather than
    containing it whole.
    """
    wanted = [_words_of(s) for s in snippets if _words_of(s)]
    if not wanted:
        return []

    regions: list[Region] = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            for column_words in _cluster_columns(page.extract_words()):
                for line in group_words_into_lines(column_words, line_tolerance):
                    line_words = _words_of(line["text"])
                    if line_words and any(_overlaps(line_words, target) for target in wanted):
                        regions.append(_span(page_number, [line]))

    return _merge_adjacent(regions, line_tolerance)


def _words_of(text: str) -> list[str]:
    return [w for w in text.lower().replace("|", " ").split() if w]


MIN_WRAPPED_FRAGMENT_WORDS = 4
"""How much of a snippet a line must carry before a partial match counts.

The two containment directions are not equally safe. Finding the snippet
*inside* a line is a true positive: a table cell reading "Skills" really is
in the rendered row "Skills    Python, SQL, Docker". The reverse -- a line
that is a fragment of a longer snippet -- is how rewrapped text gets found,
but it also matches by coincidence: a body line reading "Jane Doe" sits
inside the header snippet "Jane Doe | jane@example.com | +49 ...", and
boxing the name in the body would be wrong. Requiring a fragment to be
several words long separates the two.
"""


def _overlaps(line_words: list[str], target_words: list[str]) -> bool:
    line, target = " ".join(line_words), " ".join(target_words)

    if line == target or target in line:
        return True

    return line in target and len(line_words) >= MIN_WRAPPED_FRAGMENT_WORDS


def _merge_adjacent(regions: list[Region], line_tolerance: float) -> list[Region]:
    """Collapse stacked line boxes into one block, so a matched paragraph
    reads as a single highlighted area rather than a ladder of boxes.
    """
    merged: list[Region] = []

    for region in sorted(regions, key=lambda r: (r.page, r.top, r.x0)):
        previous = merged[-1] if merged else None
        touching = (
            previous is not None
            and previous.page == region.page
            and region.top - previous.bottom <= line_tolerance * 3
            and region.x0 < previous.x1
            and previous.x0 < region.x1
        )
        if touching:
            merged[-1] = Region(
                page=previous.page,
                x0=min(previous.x0, region.x0),
                top=min(previous.top, region.top),
                x1=max(previous.x1, region.x1),
                bottom=max(previous.bottom, region.bottom),
            )
        else:
            merged.append(region)

    return merged


def _span(page_number: int, lines: list[dict]) -> Region:
    return Region(
        page=page_number,
        x0=min(line["x0"] for line in lines),
        top=min(line["top"] for line in lines),
        x1=max(line["x1"] for line in lines),
        bottom=max(line["bottom"] for line in lines),
    )
