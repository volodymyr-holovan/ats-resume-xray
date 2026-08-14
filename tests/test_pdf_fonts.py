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
