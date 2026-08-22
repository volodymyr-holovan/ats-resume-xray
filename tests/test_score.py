from ats_xray.engine import Finding
from ats_xray.rule import get_rule
from ats_xray.score import score_resume

FOUND = {"found": True, "value": "x"}
MISSING = {"found": False, "value": None}


def fields(email=FOUND, phone=FOUND, experience=FOUND, education=FOUND, skills=FOUND):
    return {
        "name": FOUND,
        "email": email,
        "phone": phone,
        "sections": {"experience": experience, "education": education, "skills": skills},
    }


def finding(rule_id):
    return Finding(rule=get_rule(rule_id), evidence="evidence")


def test_perfect_resume_scores_100():
    breakdown = score_resume(fields(), fields(), [])

    assert breakdown.total == 100
    assert breakdown.rating == "Parses cleanly"
    assert breakdown.cap_reason is None


def test_missing_both_contact_fields_costs_the_contact_component():
    aware = naive = fields(email=MISSING, phone=MISSING)

    breakdown = score_resume(aware, naive, [])

    contact = next(c for c in breakdown.components if c.name == "Contact reachability")
    assert contact.score == 0
    assert breakdown.total == 70


def test_one_contact_field_scores_half():
    aware = naive = fields(phone=MISSING)

    contact = next(c for c in score_resume(aware, naive, []).components if c.name == "Contact reachability")

    assert contact.score == 50


def test_sections_absent_from_the_resume_are_not_counted_against_it():
    """A candidate who simply did not write a Skills section should not be
    penalised for it: the component only measures survival of sections that
    are actually there.
    """
    aware = fields(skills=MISSING)
    naive = fields(skills=MISSING)

    sections = next(c for c in score_resume(aware, naive, []).components if c.name == "Section survival")

    assert sections.score == 100
    assert "2 of 2" in sections.detail


def test_sections_component_is_unweighted_when_no_sections_exist():
    aware = naive = fields(experience=MISSING, education=MISSING, skills=MISSING)

    breakdown = score_resume(aware, naive, [])
    sections = next(c for c in breakdown.components if c.name == "Section survival")

    assert sections.weight == 0
    assert breakdown.total == 100, "an unweighted component must not drag the total down"


def test_sections_lost_only_under_naive_parsing_are_penalised():
    aware = fields()
    naive = fields(experience=MISSING)

    sections = next(c for c in score_resume(aware, naive, []).components if c.name == "Section survival")

    assert round(sections.score) == 67
    assert "experience" in sections.detail


def test_structural_findings_deduct_by_severity():
    findings = [finding("pdf_non_embedded_font")]  # medium, -10

    structure = next(
        c for c in score_resume(fields(), fields(), findings).components if c.name == "Structural integrity"
    )

    assert structure.score == 90
    assert "pdf_non_embedded_font (-10)" in structure.detail


def test_field_rules_are_not_double_counted_in_structure():
    """missing_contact_field already costs the contact component; it must not
    also deduct from structural integrity for the same problem.
    """
    aware = naive = fields(email=MISSING, phone=MISSING)
    findings = [finding("missing_contact_field")]

    structure = next(
        c for c in score_resume(aware, naive, findings).components if c.name == "Structural integrity"
    )

    assert structure.score == 100


def test_one_high_severity_finding_caps_the_total():
    findings = [finding("docx_table_content")]  # high

    breakdown = score_resume(fields(), fields(), findings)

    assert breakdown.total == 79
    assert breakdown.uncapped_total == 90
    assert "Capped at 79" in breakdown.cap_reason
    assert breakdown.rating != "Parses cleanly"


def test_two_high_severity_findings_cap_lower():
    findings = [finding("docx_table_content"), finding("docx_text_box_content")]

    breakdown = score_resume(fields(), fields(), findings)

    assert breakdown.total == 59
    assert "2 high-severity findings" in breakdown.cap_reason


def test_cap_does_not_raise_an_already_lower_score():
    """The cap is a ceiling, never a floor."""
    aware = naive = fields(email=MISSING, phone=MISSING, experience=MISSING, education=MISSING, skills=MISSING)
    findings = [finding("missing_contact_field")]

    breakdown = score_resume(aware, naive, findings)

    assert breakdown.total < 79
    assert breakdown.cap_reason is None
