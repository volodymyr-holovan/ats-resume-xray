"""Shared word-to-line grouping, used by both PDF text extraction and PDF
structural analysis: groups words into text lines by vertical proximity, in
reading order (top to bottom, then left to right within a line).
"""

DEFAULT_LINE_TOLERANCE = 3.0


def group_words_into_lines(words: list[dict], line_tolerance: float = DEFAULT_LINE_TOLERANCE) -> list[dict]:
    """Return lines as ``[{"text", "x0", "top", "x1", "bottom", "words"}, ...]``.

    The horizontal extent and the source words are included so callers that
    need to point at a line on the page (to draw a box over it) can do so
    without re-deriving the geometry.
    """
    if not words:
        return []

    ordered = sorted(words, key=lambda w: (round(w["top"], 1), w["x0"]))
    lines: list[list[dict]] = []
    for word in ordered:
        if lines and abs(word["top"] - lines[-1][-1]["top"]) <= line_tolerance:
            lines[-1].append(word)
        else:
            lines.append([word])

    return [
        {
            "text": " ".join(w["text"] for w in sorted(line, key=lambda w: w["x0"])),
            "x0": min(w["x0"] for w in line),
            "top": min(w["top"] for w in line),
            "x1": max(w["x1"] for w in line),
            "bottom": max(w["bottom"] for w in line),
            "words": sorted(line, key=lambda w: w["x0"]),
        }
        for line in lines
    ]
