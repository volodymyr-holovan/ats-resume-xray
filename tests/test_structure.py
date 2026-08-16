import docx
import pytest
from reportlab.pdfgen import canvas

from ats_xray.structure import analyze_structure


def test_analyze_structure_pdf_returns_expected_keys(tmp_path):
    pdf_path = tmp_path / "resume.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=(300, 200))
    c.setFont("Helvetica", 12)
    c.drawString(30, 150, "Resume text")
    c.save()

    result = analyze_structure(str(pdf_path))

    assert set(result.keys()) == {"non_embedded_fonts", "repeated_header_footer_lines", "textless_images"}


def test_analyze_structure_docx_returns_expected_keys(tmp_path):
    path = tmp_path / "resume.docx"
    docx.Document().save(str(path))

    result = analyze_structure(str(path))

    assert set(result.keys()) == {"headers_footers", "text_box_content", "has_table_content"}


def test_analyze_structure_rejects_unsupported_extension(tmp_path):
    path = tmp_path / "resume.txt"
    path.write_text("hello")

    with pytest.raises(ValueError):
        analyze_structure(str(path))
