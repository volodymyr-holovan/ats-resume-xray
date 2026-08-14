from reportlab.pdfgen import canvas

from ats_xray.pdf_headers_footers import _normalize, find_repeated_header_footer_lines


def test_normalize_collapses_digit_runs_and_case():
    assert _normalize("Page 1 of 3") == _normalize("PAGE 2 OF 3")


def test_normalize_distinguishes_unrelated_text():
    assert _normalize("Page 1 of 3") != _normalize("Confidential resume")


def test_find_repeated_header_footer_lines_single_page_is_noop(tmp_path):
    pdf_path = tmp_path / "single.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=(400, 300))
    c.drawString(30, 270, "Only page")
    c.save()

    assert find_repeated_header_footer_lines(str(pdf_path)) == []


def test_find_repeated_header_footer_lines_detects_repeated_header_and_footer(tmp_path):
    pdf_path = tmp_path / "two_page.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=(400, 300))
    for page_num in (1, 2):
        c.setFont("Helvetica", 12)
        c.drawString(30, 270, "Jane Doe - Resume")
        c.drawString(30, 150, f"Body content page {page_num}")
        c.drawString(30, 20, f"Page {page_num} of 2")
        if page_num == 1:
            c.showPage()
    c.save()

    findings = find_repeated_header_footer_lines(str(pdf_path))
    zones = {f["zone"] for f in findings}
    assert zones == {"header", "footer"}

    header = next(f for f in findings if f["zone"] == "header")
    assert header["pages"] == [1, 2]

    footer = next(f for f in findings if f["zone"] == "footer")
    assert footer["pages"] == [1, 2]


def test_find_repeated_header_footer_lines_ignores_non_repeating_footer_text(tmp_path):
    """Text sitting in the footer zone that differs page to page (not just
    by digits) must not be flagged: only genuine repetition matters.
    """
    pdf_path = tmp_path / "two_page.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=(400, 300))
    c.drawString(30, 20, "Unique footer note about experience")
    c.showPage()
    c.drawString(30, 20, "Completely different closing remark")
    c.save()

    assert find_repeated_header_footer_lines(str(pdf_path)) == []
