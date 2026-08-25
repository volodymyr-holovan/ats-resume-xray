from ats_xray.engine import Finding
from ats_xray.rule import get_rule
from ats_xray.score import score_resume

FOUND = {"found": True, "value": "x"}
MISSING = {"found": False, "value": None}

DATED = "Studio Nord, Hamburg  03/2019 - 08/2022"
"""The one thing a CV has that a job advert does not: employment dates.

These tests build field reports by hand, so the text has to be supplied
alongside. Anything asserting a document *is* a CV needs this; anything
asserting it is not can pass its own text or none."""


def fields(email=FOUND, phone=FOUND, experience=FOUND, education=FOUND, skills=FOUND):
    return {
        "name": FOUND,
        "email": email,
        "phone": phone,
        "sections": {"experience": experience, "education": education, "skills": skills},
    }


def finding(rule_id):
    return Finding(rule=get_rule(rule_id), evidence_key="evidence_verbatim", evidence_params={"text": "evidence"})


def test_perfect_resume_scores_100():
    breakdown = score_resume(fields(), fields(), [], DATED)

    assert breakdown.total == 100
    assert breakdown.rating_key == "rating_clean"
    assert breakdown.cap_key is None


def test_missing_both_contact_fields_costs_the_contact_component():
    aware = naive = fields(email=MISSING, phone=MISSING)

    breakdown = score_resume(aware, naive, [], DATED)

    contact = next(c for c in breakdown.components if c.name_key == "component_contact")
    assert contact.score == 0
    assert breakdown.total == 70


def test_one_contact_field_scores_half():
    aware = naive = fields(phone=MISSING)

    contact = next(c for c in score_resume(aware, naive, [], DATED).components if c.name_key == "component_contact")

    assert contact.score == 50


def test_sections_absent_from_the_resume_are_not_counted_against_it():
    """A candidate who simply did not write a Skills section should not be
    penalised for it: the component only measures survival of sections that
    are actually there.
    """
    aware = fields(skills=MISSING)
    naive = fields(skills=MISSING)

    sections = next(c for c in score_resume(aware, naive, [], DATED).components if c.name_key == "component_sections")

    assert sections.score == 100
    assert sections.detail_params["survived"] == 2
    assert sections.detail_params["total"] == 2


def test_sections_component_is_unweighted_when_no_sections_exist():
    """A CV can legitimately name none of the three sections this tool looks
    for, and the component then drops out of the average rather than scoring
    zero. Two of the three are kept here so the document still reads as a
    CV -- with none of them and only an email it would not, which is a
    different code path."""
    aware = naive = fields(skills=MISSING)

    breakdown = score_resume(aware, naive, [], DATED)
    sections = next(c for c in breakdown.components if c.name_key == "component_sections")

    assert sections.weight > 0
    assert breakdown.total == 100


def test_sections_lost_only_under_naive_parsing_are_penalised():
    aware = fields()
    naive = fields(experience=MISSING)

    sections = next(c for c in score_resume(aware, naive, [], DATED).components if c.name_key == "component_sections")

    assert round(sections.score) == 67
    assert "experience" in sections.detail_params["lost"]


def test_structural_findings_deduct_by_severity():
    findings = [finding("pdf_non_embedded_font")]  # medium, -10

    structure = next(
        c for c in score_resume(fields(), fields(), findings, DATED).components if c.name_key == "component_structure"
    )

    assert structure.score == 90
    assert "pdf_non_embedded_font (-10)" in structure.detail_params["deductions"]


def test_field_rules_are_not_double_counted_in_structure():
    """missing_contact_field already costs the contact component; it must not
    also deduct from structural integrity for the same problem.
    """
    aware = naive = fields(email=MISSING, phone=MISSING)
    findings = [finding("missing_contact_field")]

    structure = next(
        c for c in score_resume(aware, naive, findings, DATED).components if c.name_key == "component_structure"
    )

    assert structure.score == 100


def test_one_high_severity_finding_caps_the_total():
    findings = [finding("docx_table_content")]  # high

    breakdown = score_resume(fields(), fields(), findings, DATED)

    assert breakdown.total == 79
    assert breakdown.uncapped_total == 90
    assert breakdown.cap_key == "cap_reason"
    assert breakdown.cap_params["cap"] == 79
    assert breakdown.rating_key != "rating_clean"


def test_two_high_severity_findings_cap_lower():
    findings = [finding("docx_table_content"), finding("docx_text_box_content")]

    breakdown = score_resume(fields(), fields(), findings, DATED)

    assert breakdown.total == 59
    assert breakdown.cap_key == "cap_reason"
    assert breakdown.cap_params["count"] == 2


def test_cap_does_not_raise_an_already_lower_score():
    """The cap is a ceiling, never a floor.

    The sections stay found: a document with neither contact details nor any
    section is not treated as a CV at all, which is a different code path.
    """
    aware = naive = fields(email=MISSING, phone=MISSING)
    findings = [finding("missing_contact_field")]

    breakdown = score_resume(aware, naive, findings, DATED)

    assert breakdown.total < 79
    assert breakdown.cap_key is None


def test_a_document_with_no_contact_and_no_sections_is_not_scored():
    """Reported after a blank character sheet came back with a respectable
    number. It had no columns, no tables and no images, so it triggered no
    rules and scored full marks for parsing cleanly -- true, and useless."""
    nothing = fields(email=MISSING, phone=MISSING, experience=MISSING, education=MISSING, skills=MISSING)

    breakdown = score_resume(nothing, nothing, [], "a blank form")

    assert breakdown.total == 0
    assert breakdown.cap_key == "cap_reason_not_a_resume"
    assert breakdown.rating_key == "rating_not_a_resume"


def test_one_contact_detail_on_its_own_is_not_a_cv():
    """An invoice carries an accounts email and a menu carries a booking
    number. Under the one-signal rule the invoice scored 100/100."""
    only_an_email = fields(phone=MISSING, experience=MISSING, education=MISSING, skills=MISSING)

    breakdown = score_resume(only_an_email, only_an_email, [], "Invoice 4711 — total 250,00 EUR")

    assert breakdown.cap_key == "cap_reason_not_a_resume"


def test_a_contact_detail_with_one_section_is_a_cv():
    sparse = fields(phone=MISSING, education=MISSING, skills=MISSING)

    breakdown = score_resume(sparse, sparse, [], DATED)

    assert breakdown.cap_key != "cap_reason_not_a_resume"


def test_two_sections_without_any_contact_detail_are_a_cv():
    """Someone who left their phone and email off the file still wrote a CV,
    and the missing contact is exactly what the report should tell them."""
    no_contact = fields(email=MISSING, phone=MISSING, skills=MISSING)

    breakdown = score_resume(no_contact, no_contact, [], DATED)

    assert breakdown.cap_key != "cap_reason_not_a_resume"
    assert breakdown.total < 100, "missing contact details must still cost"
