from ats_xray.cli import _format_structure_report


def test_format_structure_report_pdf_with_findings():
    findings = {
        "non_embedded_fonts": ["Calibri"],
        "repeated_header_footer_lines": [{"zone": "footer", "text": "Page # of #", "pages": [1, 2]}],
        "textless_images": [{"page": 1, "bbox": (0, 0, 10, 10), "area_fraction": 0.2}],
    }

    report = _format_structure_report(findings)

    assert "Calibri" in report
    assert "footer" in report
    assert "20%" in report


def test_format_structure_report_pdf_no_findings():
    findings = {
        "non_embedded_fonts": [],
        "repeated_header_footer_lines": [],
        "textless_images": [],
    }

    report = _format_structure_report(findings)

    assert report.count("none found") == 3


def test_format_structure_report_docx():
    findings = {
        "headers_footers": {"headers": ["John Smith"], "footers": []},
        "text_box_content": ["Skills: Python"],
    }

    report = _format_structure_report(findings)

    assert "John Smith" in report
    assert "Skills: Python" in report
    assert "Footer content: none found" in report
