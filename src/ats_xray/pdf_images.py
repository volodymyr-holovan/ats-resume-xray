"""Detects images that occupy a meaningful part of a PDF page and have no
extracted text overlapping their bounding box.

Why this matters: this is exactly the pattern produced when a resume
section — a stylized name banner, a skills chart, an entire sidebar
exported from a design tool — is placed on the page as a picture instead of
real text. A naive text extractor gets nothing at all from that area, no
matter how legible the content looks to a human opening the file.

Small images (icons, bullets, dividers) are excluded via an area threshold
so this only flags images large enough to plausibly carry real content.
"""

import pdfplumber

DEFAULT_MIN_AREA_FRACTION = 0.02


def find_large_textless_images(pdf_path: str, min_area_fraction: float = DEFAULT_MIN_AREA_FRACTION) -> list[dict]:
    """Return large images with no overlapping extracted text as
    ``[{"page": int, "bbox": (x0, top, x1, bottom), "area_fraction": float}, ...]``,
    in the order they're found. Page numbers are 1-indexed.
    """
    findings = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            page_area = page.width * page.height
            if page_area <= 0:
                continue
            words = page.extract_words()

            for image in page.images:
                image_area = (image["x1"] - image["x0"]) * (image["bottom"] - image["top"])
                area_fraction = image_area / page_area
                if area_fraction < min_area_fraction:
                    continue
                if any(_overlaps(image, word) for word in words):
                    continue
                findings.append(
                    {
                        "page": page_number,
                        "bbox": (
                            round(image["x0"], 1),
                            round(image["top"], 1),
                            round(image["x1"], 1),
                            round(image["bottom"], 1),
                        ),
                        "area_fraction": round(area_fraction, 3),
                    }
                )

    return findings


def _overlaps(image: dict, word: dict) -> bool:
    return not (
        word["x1"] <= image["x0"]
        or word["x0"] >= image["x1"]
        or word["bottom"] <= image["top"]
        or word["top"] >= image["bottom"]
    )
