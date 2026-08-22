"""Renders PDF pages to images with boxes drawn over the problem areas.

The rest of the tool explains problems in words. This draws them on the page
the candidate actually recognizes, which is a much shorter path to "oh, *that*
is what's wrong".

Only PDFs can be rendered: a DOCX has no fixed page geometry until a word
processor lays it out, so there is no image to draw on and no coordinates to
draw.
"""

from dataclasses import dataclass

import pdfplumber
from PIL import Image, ImageDraw

from .engine import Finding
from .regions import Region

DEFAULT_RESOLUTION = 130

SEVERITY_COLORS = {
    "high": (220, 38, 38),
    "medium": (217, 119, 6),
    "low": (37, 99, 235),
}

BOX_WIDTH = 3
BOX_PADDING = 2.0
FILL_ALPHA = 38


@dataclass(frozen=True)
class RenderedPage:
    page_number: int
    image: Image.Image
    marked_findings: list[Finding]
    """The findings that actually have a box on this page, so a caller can
    caption the image with just those rather than repeating the full list."""


def render_pages_with_findings(
    pdf_path: str,
    findings: list[Finding],
    resolution: int = DEFAULT_RESOLUTION,
) -> list[RenderedPage]:
    """Render every page, drawing each finding's regions over it.

    Pages with no findings are still returned, so the caller can show the
    whole resume rather than only its broken parts.
    """
    rendered: list[RenderedPage] = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            image = page.to_image(resolution=resolution).original.convert("RGB")

            # Derive the scale from the image actually produced rather than
            # from resolution/72: renderers round page dimensions to whole
            # pixels, so the effective scale drifts from the nominal DPI.
            scale_x = image.width / page.width
            scale_y = image.height / page.height

            on_this_page = [f for f in findings if any(r.page == page_number for r in f.regions)]
            for finding in on_this_page:
                color = SEVERITY_COLORS.get(finding.rule.severity, SEVERITY_COLORS["low"])
                for region in finding.regions:
                    if region.page == page_number:
                        _draw_box(image, region.padded(BOX_PADDING), color, scale_x, scale_y)

            rendered.append(
                RenderedPage(page_number=page_number, image=image, marked_findings=on_this_page)
            )

    return rendered


def _draw_box(image: Image.Image, region: Region, color: tuple, scale_x: float, scale_y: float) -> None:
    box = (
        max(0, region.x0 * scale_x),
        max(0, region.top * scale_y),
        min(image.width, region.x1 * scale_x),
        min(image.height, region.bottom * scale_y),
    )
    if box[2] <= box[0] or box[3] <= box[1]:
        return

    # Tint through a separate RGBA layer so the underlying text stays legible
    # instead of being painted over.
    tint = Image.new("RGBA", image.size, (0, 0, 0, 0))
    ImageDraw.Draw(tint).rectangle(box, fill=(*color, FILL_ALPHA))
    image.paste(Image.alpha_composite(image.convert("RGBA"), tint).convert("RGB"), (0, 0))

    ImageDraw.Draw(image).rectangle(box, outline=color, width=BOX_WIDTH)
