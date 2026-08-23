import pytest

from ats_xray.engine import evaluate
from ats_xray.regions import Region

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


def _banner(width=400.0, height=60.0):
    """A wide, short image: the shape a decorative header banner takes, and
    the shape that hides text worth reading."""
    return Region(page=1, x0=0.0, top=0.0, x1=width, bottom=height)


def _portrait(width=90.0, height=120.0):
    """A taller-than-wide image in a corner: a profile photo, which hides
    nothing."""
    return Region(page=1, x0=0.0, top=0.0, x1=width, bottom=height)


def test_repeated_footer_holding_contact_details_is_high_but_a_page_number_is_low():
    """The same rule, two very different stakes: a footer nobody needs to
    read costs nothing, a footer holding the only phone number costs the
    application. Severity follows the evidence, not the rule."""
    page_numbers = {
        **EMPTY_PDF_STRUCTURE,
        "repeated_header_footer_lines": [{"zone": "footer", "text": "Page 1 of 2", "pages": [1, 2]}],
    }
    contact = {
        **EMPTY_PDF_STRUCTURE,
        "repeated_header_footer_lines": [
            {"zone": "footer", "text": "jane@example.com | +1 555 123 4567", "pages": [1, 2]}
        ],
    }
    aware = naive = field_report(email=FOUND, phone=FOUND)

    harmless = _only(evaluate("pdf", page_numbers, aware, naive), "pdf_repeated_header_footer_content")
    costly = _only(evaluate("pdf", contact, aware, naive), "pdf_repeated_header_footer_content")

    assert harmless.severity == "low"
    assert costly.severity == "high"


def test_profile_photo_is_low_but_a_banner_is_high():
    """Issue #7: flagging every profile photo as a serious problem trained
    readers to ignore the finding. A portrait-shaped image hides nothing;
    a page-wide banner is where a name and contact line go to disappear."""
    photo = {
        **EMPTY_PDF_STRUCTURE,
        "textless_images": [
            {"page": 1, "bbox": (0, 0, 90, 120), "area_fraction": 0.1, "region": _portrait()}
        ],
    }
    banner = {
        **EMPTY_PDF_STRUCTURE,
        "textless_images": [
            {"page": 1, "bbox": (0, 0, 400, 60), "area_fraction": 0.3, "region": _banner()}
        ],
    }
    aware = naive = field_report(email=FOUND, phone=FOUND)

    assert _only(evaluate("pdf", photo, aware, naive), "pdf_textless_image").severity == "low"
    assert _only(evaluate("pdf", banner, aware, naive), "pdf_textless_image").severity == "high"


def test_textless_image_without_geometry_assumes_the_worse_case():
    """When there is no bounding box to judge by, guessing "harmless" would
    silently drop a real finding; guessing "serious" only over-warns."""
    structure = {
        **EMPTY_PDF_STRUCTURE,
        "textless_images": [{"page": 1, "bbox": (0, 0, 10, 10), "area_fraction": 0.3}],
    }
    aware = naive = field_report(email=FOUND, phone=FOUND)

    assert _only(evaluate("pdf", structure, aware, naive), "pdf_textless_image").severity == "high"


def test_docx_header_is_high_with_contact_details_and_medium_without():
    plain = {**EMPTY_DOCX_STRUCTURE, "headers_footers": {"headers": ["Curriculum Vitae"], "footers": []}}
    contact = {
        **EMPTY_DOCX_STRUCTURE,
        "headers_footers": {"headers": ["jane@example.com"], "footers": []},
    }
    aware = naive = field_report(email=FOUND, phone=FOUND)

    assert _only(evaluate("docx", plain, aware, naive), "docx_header_footer_content").severity == "medium"
    assert _only(evaluate("docx", contact, aware, naive), "docx_header_footer_content").severity == "high"


def test_all_three_severity_levels_are_reachable():
    """The interface renders high, medium and low differently. A level no
    rule can ever produce is dead UI, and that was true of "low" until
    severity became evidence-based."""
    aware = naive = field_report(email=FOUND, phone=FOUND)
    structures = [
        ("pdf", {**EMPTY_PDF_STRUCTURE, "non_embedded_fonts": ["Calibri"]}),
        (
            "pdf",
            {
                **EMPTY_PDF_STRUCTURE,
                "repeated_header_footer_lines": [
                    {"zone": "footer", "text": "Page 1 of 2", "pages": [1, 2]}
                ],
            },
        ),
        ("docx", {**EMPTY_DOCX_STRUCTURE, "has_table_content": True}),
    ]

    reached = {f.severity for kind, s in structures for f in evaluate(kind, s, aware, naive)}

    assert reached == {"high", "medium", "low"}


def _only(findings, rule_id):
    return next(f for f in findings if f.rule.id == rule_id)
