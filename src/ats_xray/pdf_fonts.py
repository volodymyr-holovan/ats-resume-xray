"""Detects PDF fonts that are neither embedded nor one of the 14 standard
PDF base fonts (Helvetica, Times, Courier, Symbol, ZapfDingbats families).

Why this matters: a font that is referenced but not embedded relies on the
viewer or parser having a matching font installed, or falling back to a
substitute. That substitution can shift glyph-to-character mapping, which is
a documented cause of garbled or dropped text in automated resume parsing —
independent of anything the PDF *looks* like when opened in a viewer that
happens to have the font installed.

Standard-14 fonts are excluded from findings: every conformant PDF reader
ships with them, so referencing (without embedding) them is normal and not
a parsing risk.
"""

import pdfplumber
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdftypes import resolve1
from pdfminer.psparser import PSLiteral

from ._pdf_words import DEFAULT_LINE_TOLERANCE
from .regions import Region

STANDARD_14_FONTS = {
    "Helvetica", "Helvetica-Bold", "Helvetica-Oblique", "Helvetica-BoldOblique",
    "Courier", "Courier-Bold", "Courier-Oblique", "Courier-BoldOblique",
    "Times-Roman", "Times-Bold", "Times-Italic", "Times-BoldItalic",
    "Symbol", "ZapfDingbats",
}

_FONT_FILE_KEYS = ("FontFile", "FontFile2", "FontFile3")


def find_non_embedded_fonts(pdf_path: str) -> list[str]:
    """Return the base names of fonts used in the PDF that are not embedded
    and not one of the standard 14 base fonts, in first-seen order.
    """
    findings: list[str] = []
    seen: set[str] = set()

    with open(pdf_path, "rb") as fh:
        document = PDFDocument(PDFParser(fh))
        for page in PDFPage.create_pages(document):
            font_resources = resolve1(resolve1(page.resources).get("Font"))
            if not font_resources:
                continue
            for font_ref in font_resources.values():
                font_dict = resolve1(font_ref)
                if not isinstance(font_dict, dict):
                    continue
                base_font = _clean_base_font_name(font_dict.get("BaseFont"))
                if base_font in seen:
                    continue
                seen.add(base_font)
                if base_font not in STANDARD_14_FONTS and not _is_embedded(font_dict):
                    findings.append(base_font)

    return findings


def find_font_regions(pdf_path: str, font_names: list[str]) -> list[Region]:
    """Return one region per run of text drawn in any of ``font_names``.

    Characters are grouped into lines by vertical proximity so a paragraph
    set in a flagged font produces a handful of line-sized boxes rather than
    one box per glyph. Font names are matched after stripping the six-letter
    subset prefix, the same normalization ``find_non_embedded_fonts`` applies.
    """
    if not font_names:
        return []

    wanted = set(font_names)
    regions: list[Region] = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            flagged = [c for c in page.chars if _clean_base_font_name(c.get("fontname")) in wanted]
            for line_chars in _group_chars_into_lines(flagged):
                regions.append(
                    Region(
                        page=page_number,
                        x0=min(c["x0"] for c in line_chars),
                        top=min(c["top"] for c in line_chars),
                        x1=max(c["x1"] for c in line_chars),
                        bottom=max(c["bottom"] for c in line_chars),
                    )
                )

    return regions


def _group_chars_into_lines(chars: list[dict], line_tolerance: float = DEFAULT_LINE_TOLERANCE) -> list[list[dict]]:
    if not chars:
        return []

    ordered = sorted(chars, key=lambda c: (round(c["top"], 1), c["x0"]))
    lines: list[list[dict]] = []
    for char in ordered:
        if lines and abs(char["top"] - lines[-1][-1]["top"]) <= line_tolerance:
            lines[-1].append(char)
        else:
            lines.append([char])
    return lines


def _is_embedded(font_dict: dict) -> bool:
    """A font is embedded if its FontDescriptor carries a font program
    (FontFile/FontFile2/FontFile3). Composite (Type0) fonts store their
    descriptor one level down, on the first descendant font.
    """
    if _descriptor_has_font_file(resolve1(font_dict.get("FontDescriptor"))):
        return True

    descendants = resolve1(font_dict.get("DescendantFonts")) or []
    for descendant_ref in descendants:
        descendant = resolve1(descendant_ref)
        if isinstance(descendant, dict) and _descriptor_has_font_file(
            resolve1(descendant.get("FontDescriptor"))
        ):
            return True

    return False


def _descriptor_has_font_file(descriptor: object) -> bool:
    return isinstance(descriptor, dict) and any(key in descriptor for key in _FONT_FILE_KEYS)


def _clean_base_font_name(base_font: PSLiteral | bytes | str | None) -> str:
    """Normalize a PDF BaseFont value to a plain name, stripping the
    six-letter subset prefix (e.g. "ABCDEF+Calibri" -> "Calibri") that
    subsetted, embedded fonts carry.
    """
    if base_font is None:
        return "Unknown"
    if isinstance(base_font, PSLiteral):
        name = base_font.name
    elif isinstance(base_font, bytes):
        name = base_font.decode("latin-1", errors="replace")
    else:
        name = str(base_font)

    if len(name) > 7 and name[6] == "+" and name[:6].isalpha() and name[:6].isupper():
        name = name[7:]
    return name
