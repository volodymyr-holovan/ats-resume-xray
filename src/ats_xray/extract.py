"""PDF text extraction, in two flavors.

``extract_naive`` mimics a layout-blind parser: words are sorted purely by
vertical position, so a two-column resume gets its left and right column
text interleaved line by line.

``extract_layout_aware`` detects column boundaries first, then reads each
column top-to-bottom before moving to the next one — the way a human would.

The column-clustering and line-building logic is split into pure functions
(``_cluster_columns``, ``_words_to_text``) that operate on plain word dicts,
so they can be unit-tested without opening a real PDF.
"""

import pdfplumber

DEFAULT_MIN_COLUMN_GAP = 20.0
DEFAULT_LINE_TOLERANCE = 3.0


def extract_naive(pdf_path: str) -> str:
    """Extract text the way a basic parser would: pdfplumber's default
    top-to-bottom, left-to-right word ordering, with no column detection.
    """
    pages_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            pages_text.append(page.extract_text() or "")
    return "\n\n".join(pages_text)


def extract_layout_aware(pdf_path: str, min_gap: float = DEFAULT_MIN_COLUMN_GAP) -> str:
    """Extract text column by column, so multi-column resumes read in the
    order a human intends instead of interleaved row by row.
    """
    pages_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            words = page.extract_words()
            columns = _cluster_columns(words, min_gap=min_gap)
            columns_text = [_words_to_text(col) for col in columns]
            pages_text.append("\n\n".join(text for text in columns_text if text))
    return "\n\n".join(pages_text)


def _cluster_columns(words: list[dict], min_gap: float = DEFAULT_MIN_COLUMN_GAP) -> list[list[dict]]:
    """Group words into left-to-right columns.

    Merges the horizontal spans (x0, x1) of all words into intervals, treating
    a horizontal gap wider than ``min_gap`` as a real column boundary rather
    than ordinary word spacing. Each word is then assigned to the interval
    that contains it.
    """
    if not words:
        return []

    spans = sorted((w["x0"], w["x1"]) for w in words)
    merged = [list(spans[0])]
    for x0, x1 in spans[1:]:
        if x0 - merged[-1][1] > min_gap:
            merged.append([x0, x1])
        else:
            merged[-1][1] = max(merged[-1][1], x1)

    columns = []
    for start, end in merged:
        col_words = [w for w in words if w["x0"] >= start - 0.1 and w["x1"] <= end + 0.1]
        if col_words:
            columns.append(col_words)
    return columns


def _words_to_text(words: list[dict], line_tolerance: float = DEFAULT_LINE_TOLERANCE) -> str:
    """Sort words into reading order (top to bottom, then left to right
    within a line) and join them into text lines.
    """
    if not words:
        return ""

    ordered = sorted(words, key=lambda w: (round(w["top"], 1), w["x0"]))

    lines: list[list[dict]] = []
    for word in ordered:
        if lines and abs(word["top"] - lines[-1][-1]["top"]) <= line_tolerance:
            lines[-1].append(word)
        else:
            lines.append([word])

    return "\n".join(
        " ".join(w["text"] for w in sorted(line, key=lambda w: w["x0"]))
        for line in lines
    )
