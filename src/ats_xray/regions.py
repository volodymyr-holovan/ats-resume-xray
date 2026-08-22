"""Page regions: where on the page a finding actually is.

A ``Region`` is a rectangle in PDF user-space coordinates (points, origin at
the top-left of the page as pdfplumber reports them, so ``top`` grows
downward). Findings carry regions so the app can draw them over a rendered
image of the page instead of only describing the problem in prose.

DOCX has no page geometry until it is laid out by a word processor, so DOCX
findings carry no regions. That is a real limitation, not an oversight: the
visual overlay is a PDF-only feature.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Region:
    """A rectangle on one page, in PDF points. ``page`` is 1-indexed."""

    page: int
    x0: float
    top: float
    x1: float
    bottom: float

    def padded(self, amount: float) -> "Region":
        """Grow the rectangle on every side, so a drawn box sits slightly
        outside the text rather than clipping its glyphs.
        """
        return Region(
            page=self.page,
            x0=self.x0 - amount,
            top=self.top - amount,
            x1=self.x1 + amount,
            bottom=self.bottom + amount,
        )


def bounding_region(regions: list[Region]) -> Region | None:
    """Merge regions that share a page into one enclosing rectangle. Returns
    None for an empty list. Raises ValueError if the regions span pages,
    since a single rectangle cannot describe that.
    """
    if not regions:
        return None

    pages = {r.page for r in regions}
    if len(pages) > 1:
        raise ValueError(f"Cannot merge regions across pages: {sorted(pages)}")

    return Region(
        page=regions[0].page,
        x0=min(r.x0 for r in regions),
        top=min(r.top for r in regions),
        x1=max(r.x1 for r in regions),
        bottom=max(r.bottom for r in regions),
    )


def region_from_words(page_number: int, words: list[dict]) -> Region | None:
    """Build the enclosing region for a group of pdfplumber word dicts."""
    if not words:
        return None
    return Region(
        page=page_number,
        x0=min(w["x0"] for w in words),
        top=min(w["top"] for w in words),
        x1=max(w["x1"] for w in words),
        bottom=max(w["bottom"] for w in words),
    )
