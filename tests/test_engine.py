import pytest

from ats_xray.engine import evaluate

FOUND = {"found": True, "value": "x"}
MISSING = {"found": False, "value": None}


def field_report(email=MISSING, phone=MISSING, experience=MISSING, education=MISSING, skills=MISSING):
    return {
        "name": FOUND,
        "email": email,
        "phone": phone,
        "sections": {"experience": experience, "education": education, "skills": skills},
    }


EMPTY_PDF_STRUCTURE = {
    "non_embedded_fonts": [],
    "repeated_header_footer_lines": [],
    "textless_images": [],
}

EMPTY_DOCX_STRUCTURE = {
    "headers_footers": {"headers": [], "footers": []},
    "text_box_content": [],
    "has_table_content": False,
}


def test_evaluate_pdf_no_signals_triggers_nothing():
    aware = field_report(email=FOUND, phone=FOUND, experience=FOUND, education=FOUND, skills=FOUND)
    naive = field_report(email=FOUND, phone=FOUND, experience=FOUND, education=FOUND, skills=FOUND)

    findings = evaluate("pdf", EMPTY_PDF_STRUCTURE, aware, naive)

    assert findings == []


def test_evaluate_pdf_non_embedded_font_triggers():
    structure = {**EMPTY_PDF_STRUCTURE, "non_embedded_fonts": ["Calibri"]}
    aware = naive = field_report(email=FOUND, phone=FOUND)

    findings = evaluate("pdf", structure, aware, naive)

    ids = {f.rule.id for f in findings}
    assert "pdf_non_embedded_font" in ids
    match = next(f for f in findings if f.rule.id == "pdf_non_embedded_font")
    assert "Calibri" in match.evidence


def test_evaluate_pdf_repeated_header_footer_triggers():
    structure = {
        **EMPTY_PDF_STRUCTURE,
        "repeated_header_footer_lines": [{"zone": "footer", "text": "Page # of #", "pages": [1, 2]}],
    }
    aware = naive = field_report(email=FOUND, phone=FOUND)

    findings = evaluate("pdf", structure, aware, naive)

    assert any(f.rule.id == "pdf_repeated_header_footer_content" for f in findings)


def test_evaluate_pdf_textless_image_triggers():
    structure = {
        **EMPTY_PDF_STRUCTURE,
        "textless_images": [{"page": 1, "bbox": (0, 0, 10, 10), "area_fraction": 0.3}],
    }
    aware = naive = field_report(email=FOUND, phone=FOUND)

    findings = evaluate("pdf", structure, aware, naive)

    assert any(f.rule.id == "pdf_textless_image" for f in findings)


def test_evaluate_docx_header_footer_content_triggers():
    structure = {**EMPTY_DOCX_STRUCTURE, "headers_footers": {"headers": ["Jane Doe"], "footers": []}}
    aware = naive = field_report(email=FOUND, phone=FOUND)

    findings = evaluate("docx", structure, aware, naive)

    assert any(f.rule.id == "docx_header_footer_content" for f in findings)


def test_evaluate_docx_text_box_content_triggers():
    structure = {**EMPTY_DOCX_STRUCTURE, "text_box_content": ["Skills: Python"]}
    aware = naive = field_report(email=FOUND, phone=FOUND)

    findings = evaluate("docx", structure, aware, naive)

    assert any(f.rule.id == "docx_text_box_content" for f in findings)


def test_evaluate_docx_table_content_triggers():
    structure = {**EMPTY_DOCX_STRUCTURE, "has_table_content": True}
    aware = naive = field_report(email=FOUND, phone=FOUND)

    findings = evaluate("docx", structure, aware, naive)

    assert any(f.rule.id == "docx_table_content" for f in findings)


def test_evaluate_missing_contact_field_triggers_when_both_absent():
    aware = naive = field_report(email=MISSING, phone=MISSING)

    findings = evaluate("pdf", EMPTY_PDF_STRUCTURE, aware, naive)

    assert any(f.rule.id == "missing_contact_field" for f in findings)


def test_evaluate_missing_contact_field_does_not_trigger_if_either_present():
    aware = naive = field_report(email=FOUND, phone=MISSING)

    findings = evaluate("pdf", EMPTY_PDF_STRUCTURE, aware, naive)

    assert not any(f.rule.id == "missing_contact_field" for f in findings)


def test_evaluate_section_missing_under_naive_parsing_triggers():
    aware = field_report(email=FOUND, phone=FOUND, experience=FOUND)
    naive = field_report(email=FOUND, phone=FOUND, experience=MISSING)

    findings = evaluate("pdf", EMPTY_PDF_STRUCTURE, aware, naive)

    match = next(f for f in findings if f.rule.id == "section_missing_under_naive_parsing")
    assert "experience" in match.evidence


def test_evaluate_section_missing_does_not_trigger_when_truly_absent_from_resume():
    """A section absent from both naive and layout-aware extraction means the
    candidate simply didn't include it (e.g. no Education section) — not a
    parsing risk, so this must not be flagged.
    """
    aware = field_report(email=FOUND, phone=FOUND, education=MISSING)
    naive = field_report(email=FOUND, phone=FOUND, education=MISSING)

    findings = evaluate("pdf", EMPTY_PDF_STRUCTURE, aware, naive)

    assert not any(f.rule.id == "section_missing_under_naive_parsing" for f in findings)


def test_evaluate_unknown_file_type_raises():
    aware = naive = field_report(email=FOUND, phone=FOUND)
    with pytest.raises(ValueError):
        evaluate("txt", {}, aware, naive)
