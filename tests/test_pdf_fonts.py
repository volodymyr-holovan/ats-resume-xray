from pathlib import Path

import golden_generators as generators
import reportlab
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from ats_xray.pdf_fonts import _clean_base_font_name, _is_embedded, find_non_embedded_fonts


def test_clean_base_font_name_strips_subset_prefix():
    assert _clean_base_font_name("ABCDEF+Calibri") == "Calibri"


def test_clean_base_font_name_leaves_plain_name_untouched():
    assert _clean_base_font_name("Helvetica") == "Helvetica"


def test_clean_base_font_name_handles_none():
    assert _clean_base_font_name(None) == "Unknown"


def test_is_embedded_true_with_font_file():
    assert _is_embedded({"FontDescriptor": {"FontFile2": b"..."}}) is True


def test_is_embedded_false_without_font_file():
    assert _is_embedded({"FontDescriptor": {"Flags": 32}}) is False


def test_is_embedded_false_without_descriptor():
    assert _is_embedded({}) is False


def test_is_embedded_true_via_descendant_font():
    font_dict = {"DescendantFonts": [{"FontDescriptor": {"FontFile3": b"..."}}]}
    assert _is_embedded(font_dict) is True


def test_find_non_embedded_fonts_standard_font_not_flagged(tmp_path):
    pdf_path = tmp_path / "standard_font.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=(300, 200))
    c.setFont("Helvetica", 12)
    c.drawString(30, 150, "Standard font resume text")
    c.save()

    assert find_non_embedded_fonts(str(pdf_path)) == []


def test_a_font_that_is_only_referenced_is_flagged(tmp_path):
    """The case the rule exists for, end to end rather than on a dict.

    Everything above this tests a helper on a literal. Until this fixture
    existed nothing put a real file through ``find_non_embedded_fonts`` and
    got a finding back, because no library here can write one: reportlab
    embeds every TrueType face it is handed and references only the standard
    fourteen, which are exempt. ``golden_generators`` assembles the PDF by
    hand for exactly this reason.
    """
    pdf_path = tmp_path / "referenced_only.pdf"
    generators.pdf_unembedded_font(pdf_path)

    assert find_non_embedded_fonts(str(pdf_path)) == ["Frutiger-Light"]


def test_an_embedded_subset_font_is_not_flagged(tmp_path):
    """The subset prefix, on a real file rather than on a string.

    An embedded font is usually subsetted, and a subsetted font's BaseFont
    carries six random capitals and a plus sign in front of its name. The
    stripping is unit-tested above on the literal "ABCDEF+Calibri"; this
    proves the whole path agrees with it when the prefix is one reportlab
    generated itself, whatever six letters it chose this time.
    """
    vera = Path(reportlab.__file__).parent / "fonts" / "Vera.ttf"
    pdfmetrics.registerFont(TTFont("Vera", str(vera)))

    pdf_path = tmp_path / "embedded.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=(300, 200))
    c.setFont("Vera", 12)
    c.drawString(30, 150, "Embedded and subsetted")
    c.save()

    assert find_non_embedded_fonts(str(pdf_path)) == []
