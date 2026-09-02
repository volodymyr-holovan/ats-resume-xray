"""When a skill was last used, and what to fix first.

A keyword matcher treats "Photoshop, 2011-2013" and "Photoshop, still doing
it" as the same fact. An employer does not, and neither does the interview.
"""

from datetime import date

import pytest

from ats_xray.match import evaluate_match
from ats_xray.recency import find_dated_entries, is_stale, last_used, years_since
from ats_xray.vacancy import Requirement

TODAY = date(2026, 9, 1)

CV = """Anna Muster
anna@example.com | 040 1234567

Berufserfahrung
03/2019 - heute   Studio Nord, Hamburg
Konzeption und Gestaltung mit Figma

01/2010 - 12/2014  Druckerei Alt
Satz und Reinzeichnung mit Photoshop und InDesign

Ausbildung
10/2006 - 09/2009  HAW Hamburg
"""


def test_each_dated_block_becomes_an_entry():
    entries = find_dated_entries(CV, TODAY)

    assert len(entries) == 3
    assert entries[0].is_current
    assert not entries[1].is_current


def test_a_skill_in_a_running_entry_is_current():
    entries = find_dated_entries(CV, TODAY)

    assert last_used("figma", entries) == 0
    assert not is_stale("figma", CV, entries, TODAY)


def test_a_skill_only_in_an_old_entry_is_stale():
    entries = find_dated_entries(CV, TODAY)

    assert is_stale("adobe", CV, entries, TODAY)
    assert years_since(last_used("adobe", entries), TODAY) == 11


def test_a_skill_listed_under_skills_is_never_stale():
    """Listing a skill is a claim about the present. Telling the candidate
    otherwise would be arguing with them about their own CV, on the
    strength of a date that belongs to a job rather than to the skill."""
    with_section = CV + "\nKenntnisse\nPhotoshop, InDesign\n"
    entries = find_dated_entries(with_section, TODAY)

    assert not is_stale("adobe", with_section, entries, TODAY)


def test_a_cv_with_no_dates_at_all_produces_no_staleness():
    """No dates is not evidence of age. Guessing here would put a warning
    on every CV that writes its history without a date column."""
    undated = "Anna Muster\nanna@example.com\n\nBerufserfahrung\nStudio Nord — Photoshop"
    entries = find_dated_entries(undated, TODAY)

    assert entries == []
    assert not is_stale("adobe", undated, entries, TODAY)


def test_the_report_carries_the_stale_matches():
    requirements = [
        Requirement(kind="skill", key="adobe", label="Adobe Creative Suite", must=True),
        Requirement(kind="skill", key="figma", label="Figma", must=True),
    ]

    report = evaluate_match(requirements, CV, CV, today=TODAY)

    assert [o.requirement.key for o in report.stale] == ["adobe"]
    assert report.score == 100, "a stale match is still a match"


def test_a_stale_match_says_how_long_ago():
    requirements = [Requirement(kind="skill", key="adobe", label="Adobe Creative Suite", must=True)]

    outcome = evaluate_match(requirements, CV, CV, today=TODAY).outcomes[0]

    assert outcome.note_key == "match_note_skill_stale"
    assert outcome.note_params["years"] == 11


def test_a_skill_the_parser_cannot_see_outranks_a_stale_one():
    """Both are true and only one fits on the line. Losing the match
    outright beats being asked about it in an interview."""
    requirements = [Requirement(kind="skill", key="adobe", label="Adobe Creative Suite", must=True)]
    # A naive read that recovered the page but lost the entry holding the
    # skill. Empty would mean "not supplied", which is a different thing.
    naive = "Anna Muster\nanna@example.com\n\nBerufserfahrung\nStudio Nord"

    outcome = evaluate_match(requirements, CV, naive_text=naive, today=TODAY).outcomes[0]

    assert outcome.stale, "the fixture is meant to be stale as well"
    assert outcome.at_risk
    assert outcome.note_key == "match_note_skill_at_risk"


# --------------------------------------------------------------------------
# What to fix first
# --------------------------------------------------------------------------


def test_gains_are_ordered_by_what_they_are_worth():
    requirements = [
        Requirement(kind="skill", key="kubernetes", label="Kubernetes", must=True),
        Requirement(kind="skill", key="terraform", label="Terraform", must=False),
        Requirement(kind="skill", key="figma", label="Figma", must=True),
    ]

    report = evaluate_match(requirements, CV, CV, today=TODAY)

    assert [o.requirement.label for o, _ in report.gains] == ["Kubernetes", "Terraform"]
    assert report.gains[0][1] > report.gains[1][1], "a must-have is worth more than a nice-to-have"


def test_a_gain_is_exactly_what_meeting_it_would_add():
    """The score is a weighted average, so this is arithmetic rather than
    an estimate -- and a promise the reader can check by editing their CV
    and running it again."""
    requirements = [
        Requirement(kind="skill", key="kubernetes", label="Kubernetes", must=True),
        Requirement(kind="skill", key="figma", label="Figma", must=True),
    ]

    report = evaluate_match(requirements, CV, CV, today=TODAY)
    outcome, points = report.gains[0]

    assert report.score + points == 100


def test_a_fully_met_advert_offers_no_gains():
    requirements = [Requirement(kind="skill", key="figma", label="Figma", must=True)]

    report = evaluate_match(requirements, CV, CV, today=TODAY)

    assert report.gains == ()


@pytest.mark.parametrize("count", [1, 5, 20])
def test_the_list_stays_short_however_much_is_missing(count):
    """A list of everything missing is the gaps column, which is already on
    screen. This one answers "what first", and an answer with twenty items
    is not an answer."""
    requirements = [
        Requirement(kind="skill", key=f"custom:missing{i}", label=f"Missing {i}", must=True)
        for i in range(count)
    ]

    report = evaluate_match(requirements, CV, CV, today=TODAY)

    assert len(report.gains) <= 3
