"""The one ordered list of what to change.

The report says what is wrong three times over — a finding names the fault,
its fix list gives the steps, the match columns say what the advert wanted
— and none of those is a plan. What is asserted here is the merge: that
everything worth doing appears once, in the order it costs most to leave
undone, and that each line says what the document should end up looking
like rather than which menu to open, because the block is copied off the
page and read somewhere the menu does not exist.
"""

from datetime import date

import pytest

import ats_xray.rules  # noqa: F401  (registers the rule set)
from ats_xray.action_plan import build_plan
from ats_xray.engine import Finding
from ats_xray.i18n import UI_LANGUAGES, rule_fixes, rule_plan, t
from ats_xray.match import evaluate_match
from ats_xray.rule import get_rule
from ats_xray.vacancy import Requirement

TODAY = date(2026, 9, 1)

CV = """Anna Muster
anna@example.com | 040 1234567

Berufserfahrung
03/2019 - heute   Studio Nord, Hamburg
Gestaltung mit Figma

01/2010 - 12/2014  Druckerei Alt
Satz und Reinzeichnung mit Photoshop und InDesign
"""


def finding(rule_id, severity=None):
    rule = get_rule(rule_id)
    return Finding(
        rule=rule,
        evidence_key="evidence_verbatim",
        evidence_params={"text": "x"},
        severity_override=severity,
    )


def test_an_empty_report_produces_an_empty_plan():
    """Nothing wrong, nothing to say. A plan that always finds something to
    tell you is a plan nobody reads twice."""
    assert build_plan([], None) == []


def test_structure_comes_before_content():
    """A skill the parser cannot see is worth nothing however well it
    matches, so a layout fault outranks a missing keyword — whatever the
    keyword is worth."""
    requirements = [Requirement(kind="skill", key="kubernetes", label="Kubernetes", must=True)]
    report = evaluate_match(requirements, CV, CV, today=TODAY)

    steps = build_plan([finding("docx_table_content")], report)

    assert steps[0].kind == "fix"
    assert any(step.kind == "add" for step in steps)
    assert [s.kind for s in steps].index("fix") < [s.kind for s in steps].index("add")


def test_the_most_serious_finding_is_first():
    steps = build_plan(
        [finding("pdf_non_embedded_font"), finding("docx_table_content")], None
    )

    assert [step.rule_id for step in steps] == ["docx_table_content", "pdf_non_embedded_font"]


def test_gains_keep_the_order_they_were_ranked_in():
    """The gaps column treats a blocking requirement and a nice-to-have
    alike. The plan does not, and it inherits that ranking rather than
    computing a second one."""
    requirements = [
        Requirement(kind="skill", key="kubernetes", label="Kubernetes", must=True),
        Requirement(kind="skill", key="terraform", label="Terraform", must=False),
    ]
    report = evaluate_match(requirements, CV, CV, today=TODAY)

    steps = [s for s in build_plan([], report) if s.kind == "add"]

    assert [s.params["item"] for s in steps] == [o.requirement.label for o, _ in report.gains]
    assert steps[0].params["points"] >= steps[-1].params["points"]


def test_a_stale_skill_is_named_with_how_long_ago():
    requirements = [Requirement(kind="skill", key="adobe", label="Adobe Creative Suite", must=True)]
    report = evaluate_match(requirements, CV, CV, today=TODAY)

    refresh = [s for s in build_plan([], report) if s.kind == "refresh"]

    assert refresh and refresh[0].params["item"] == "Adobe Creative Suite"
    assert refresh[0].params["years"] > 6


def test_without_an_advert_the_plan_is_the_structural_half_alone():
    """No pasted advert means nothing is known about content, and guessing
    at it would be inventing requirements the reader never saw."""
    steps = build_plan([finding("docx_table_content")], None)

    assert {step.kind for step in steps} == {"fix"}


# --------------------------------------------------------------------------
# What the reader actually reads
# --------------------------------------------------------------------------


@pytest.mark.parametrize("language", list(UI_LANGUAGES))
def test_every_step_renders_a_real_sentence(language):
    """A step is a key and some parameters; if either drifts the reader
    gets a bracketed placeholder in the box they are about to copy."""
    requirements = [
        Requirement(kind="skill", key="kubernetes", label="Kubernetes", must=True),
        Requirement(kind="skill", key="adobe", label="Adobe Creative Suite", must=True),
    ]
    report = evaluate_match(requirements, CV, CV, today=TODAY)
    steps = build_plan([finding("docx_table_content")], report)

    for step in steps:
        if step.kind == "fix":
            sentence = rule_plan(step.rule_id, language)
        else:
            sentence = t(step.key, language, **step.params)

        assert sentence
        assert "{" not in sentence
        assert not sentence.startswith("[")


def test_a_fix_step_says_the_outcome_rather_than_the_route_to_it():
    """The block is copied off the page, so it has to survive the trip.

    The fix list under the finding walks one application: click here, then
    this submenu, then that checkbox. That is the right answer for someone
    sitting in that application and useless to a reader in another editor
    -- or to a model handed the CV and this list, which can act on what the
    document should look like and cannot click anything."""
    steps = build_plan([finding("docx_table_content")], None)

    assert steps[0].rule_id == "docx_table_content"
    assert "Tabellenlayout" in rule_fixes("docx_table_content", "de")[0]
    assert "Tabellenlayout" not in rule_plan("docx_table_content", "de")


def test_a_skill_that_is_both_invisible_and_old_still_reports_its_age():
    """Which note wins is a presentation decision. The at-risk sentence has
    no years in its parameters, so a plan reading them from there told the
    reader a skill last used eleven years ago had ended "0 years ago" --
    a false statement produced by asking the wrong object."""
    requirements = [Requirement(kind="skill", key="adobe", label="Adobe Creative Suite", must=True)]
    naive = "Anna Muster\nanna@example.com\n\nBerufserfahrung\nStudio Nord"

    outcome = evaluate_match(requirements, CV, naive_text=naive, today=TODAY).outcomes[0]

    assert outcome.at_risk and outcome.stale
    assert outcome.note_key == "match_note_skill_at_risk"
    assert outcome.stale_years > 6, "the age is carried whichever sentence is shown"


def test_the_refresh_step_never_says_zero_years():
    requirements = [Requirement(kind="skill", key="adobe", label="Adobe Creative Suite", must=True)]
    naive = "Anna Muster\nanna@example.com\n\nBerufserfahrung\nStudio Nord"
    report = evaluate_match(requirements, CV, naive_text=naive, today=TODAY)

    refresh = [s for s in build_plan([], report) if s.kind == "refresh"]

    assert refresh
    assert all(step.params["years"] > 0 for step in refresh)


def test_one_remedy_is_not_listed_twice():
    """A CV reachable only through a link has no email in its text either,
    so both rules fire and both open with the same instruction."""
    steps = build_plan(
        [finding("missing_contact_field"), finding("contact_only_as_link")], None
    )

    assert [step.rule_id for step in steps] == ["missing_contact_field"]


def test_the_link_rule_still_speaks_when_it_is_the_only_one():
    steps = build_plan([finding("contact_only_as_link")], None)

    assert [step.rule_id for step in steps] == ["contact_only_as_link"]
