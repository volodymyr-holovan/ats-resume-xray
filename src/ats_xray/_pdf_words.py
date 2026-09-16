"""Shared word-to-line grouping, used by both PDF text extraction and PDF
structural analysis: groups words into text lines by vertical proximity, in
reading order (top to bottom, then left to right within a line).
"""

DEFAULT_LINE_TOLERANCE = 3.0


def group_boxes_into_lines(
    boxes: list[dict], line_tolerance: float = DEFAULT_LINE_TOLERANCE
) -> list[list[dict]]:
    """Group anything pdfplumber gives a ``top`` and an ``x0`` into lines.

    Words are what most callers have; the font check works a level down, on
    characters, because a single line can be set in two fonts and only one of
    them is the unembedded one. The grouping is the same question either way
    -- which of these boxes sit at the same height -- and it was written out
    once for each, which is one place too many for a rule about what counts
    as the same line.
    """
    ordered = sorted(boxes, key=lambda box: (round(box["top"], 1), box["x0"]))
    lines: list[list[dict]] = []
    for box in ordered:
        if lines and abs(box["top"] - lines[-1][-1]["top"]) <= line_tolerance:
            lines[-1].append(box)
        else:
            lines.append([box])
    return lines


def group_words_into_lines(words: list[dict], line_tolerance: float = DEFAULT_LINE_TOLERANCE) -> list[dict]:
    """Return lines as ``[{"text", "x0", "top", "x1", "bottom", "words"}, ...]``.

    The horizontal extent and the source words are included so callers that
    need to point at a line on the page (to draw a box over it) can do so
    without re-deriving the geometry.
    """
    return [
        {
            "text": " ".join(w["text"] for w in sorted(line, key=lambda w: w["x0"])),
            "x0": min(w["x0"] for w in line),
            "top": min(w["top"] for w in line),
            "x1": max(w["x1"] for w in line),
            "bottom": max(w["bottom"] for w in line),
            "words": sorted(line, key=lambda w: w["x0"]),
        }
        for line in group_boxes_into_lines(words, line_tolerance)
    ]
