from datetime import date

from ats_xray.match import MUST_WEIGHT, NICE_WEIGHT, evaluate_match
from ats_xray.vacancy import Requirement, parse_vacancy

TODAY = date(2026, 8, 24)

CV = """Volodymyr Holovan
volodymyr@example.com | +49 160 4562730

Ausbildung
Bachelor of Science, Informatik
Nationale Technische Universitaet, 09/2021 - 06/2025

Berufserfahrung
Technischer Support, Syke, 09/2023 - 06/2026
Betrieb und Wartung von Veranstaltungstechnik

Kenntnisse
Python, C#, .NET Framework, SQL, MySQL, Docker, Linux, Git

Sprachen
Deutsch - B2 (telc), Englisch - C1
"""


def _skill(key, must=True, label=None):
    return Requirement(kind="skill", key=key, label=label or key, must=must)


def _match(requirements, cv=CV, naive=None):
    return evaluate_match(requirements, cv, cv if naive is None else naive, today=TODAY)


def test_a_skill_present_in_the_cv_is_met():
    report = _match([_skill("docker")])

    assert report.outcomes[0].status == "met"
    assert report.score == 100


def test_a_skill_absent_from_the_cv_is_missing():
    report = _match([_skill("kubernetes")])

    assert report.outcomes[0].status == "missing"
    assert report.score == 0


def test_required_items_outweigh_preferred_ones():
    """Missing one blocking requirement has to cost more than collecting a
    handful of optional extras, or the score rewards the wrong things."""
    report = _match([_skill("kubernetes", must=True), _skill("docker", must=False)])

    expected = round(NICE_WEIGHT / (MUST_WEIGHT + NICE_WEIGHT) * 100)
    assert report.score == expected


def test_missing_required_items_are_listed_separately():
    report = _match([_skill("kubernetes"), _skill("terraform", must=False)])

    assert [o.requirement.key for o in report.missing_must] == ["kubernetes"]


# ------------------------------------------------------------------ degrees
def test_a_higher_degree_satisfies_a_lower_requirement():
    """The comparison is a level comparison, not a keyword one: a Master
    reported as "missing Bachelor" would be obviously wrong to any reader
    and would sink trust in the whole report."""
    cv = "Ausbildung\nMasterabschluss Informatik\n"
    requirement = Requirement(
        kind="education", key="bachelor", label="Bachelor", must=True, detail={"level": "bachelor"}
    )

    assert _match([requirement], cv=cv).outcomes[0].status == "met"


def test_a_lower_degree_is_partial_when_equivalents_are_accepted():
    requirement = Requirement(
        kind="education",
        key="master",
        label="Master",
        must=False,
        detail={"level": "master", "equivalent_accepted": True},
    )

    assert _match([requirement]).outcomes[0].status == "partial"


def test_a_lower_degree_is_missing_when_the_degree_is_a_gate():
    requirement = Requirement(
        kind="education", key="master", label="Master", must=True, detail={"level": "master"}
    )

    assert _match([requirement]).outcomes[0].status == "missing"


def test_the_right_level_in_the_wrong_field_is_partial():
    requirement = Requirement(
        kind="education",
        key="bachelor",
        label="Bachelor",
        must=True,
        detail={"level": "bachelor", "field": "business"},
    )

    assert _match([requirement]).outcomes[0].status == "partial"


# --------------------------------------------------------------- experience
def test_experience_is_counted_from_the_experience_section_only():
    """Study dates sit in the education section. Counting them as
    professional experience would give every graduate several years they
    have not worked."""
    requirement = Requirement(
        kind="experience", key="years", label="2 years", must=True, detail={"years": 2}
    )
    outcome = _match([requirement]).outcomes[0]

    assert outcome.status == "met"
    # 09/2023 - 06/2026 is 34 months; the 2021-2025 degree is not added.
    assert outcome.note_params["have"] == 2.8


def test_slightly_short_experience_is_partial_rather_than_missing():
    requirement = Requirement(
        kind="experience", key="years", label="4 years", must=True, detail={"years": 4}
    )

    assert _match([requirement]).outcomes[0].status == "partial"


def test_far_short_experience_is_missing():
    requirement = Requirement(
        kind="experience", key="years", label="10 years", must=True, detail={"years": 10}
    )

    assert _match([requirement]).outcomes[0].status == "missing"


# ---------------------------------------------------------------- languages
def test_a_higher_language_level_satisfies_a_lower_one():
    requirement = Requirement(
        kind="language", key="en", label="EN B2", must=True, detail={"level": "b2"}
    )

    assert _match([requirement]).outcomes[0].status == "met"


def test_one_level_short_is_partial():
    requirement = Requirement(
        kind="language", key="de", label="DE C1", must=True, detail={"level": "c1"}
    )
    outcome = _match([requirement]).outcomes[0]

    assert outcome.status == "partial"
    assert outcome.note_params == {"lang": "DE", "have": "B2", "want": "C1"}


def test_two_levels_short_is_missing():
    requirement = Requirement(
        kind="language", key="de", label="DE C2", must=True, detail={"level": "c2"}
    )

    assert _match([requirement]).outcomes[0].status == "missing"


# ---------------------------------------------------- parser-visibility tie-in
def test_a_match_only_the_layout_aware_read_can_see_is_flagged():
    """The feature this tool has and a generic keyword matcher does not: a
    requirement met only in the layout-aware text would not count for an
    employer whose software reads the file the naive way."""
    naive_without_docker = CV.replace("Docker, ", "")
    report = _match([_skill("docker")], naive=naive_without_docker)

    assert report.outcomes[0].status == "met"
    assert report.outcomes[0].at_risk
    assert report.at_risk


def test_a_match_visible_to_both_reads_is_not_flagged():
    report = _match([_skill("docker")])

    assert not report.at_risk


# ------------------------------------------------------------ typed keywords
def test_a_keyword_the_reader_typed_is_searched_as_a_phrase():
    """Custom keywords have no lexicon entry, so they fall back to a phrase
    search -- with the same tolerance for German inflection."""
    typed = Requirement(kind="skill", key="custom:veranstaltungstechnik", label="Veranstaltungstechnik", must=True)

    assert _match([typed]).outcomes[0].status == "met"


def test_a_custom_keyword_absent_from_the_cv_is_missing():
    typed = Requirement(kind="skill", key="custom:kernphysik", label="Kernphysik", must=True)

    assert _match([typed]).outcomes[0].status == "missing"


# ------------------------------------------------------------------- extras
def test_skills_the_advert_did_not_ask_for_are_reported_separately():
    report = _match([_skill("docker")])

    assert "python" in report.extras
    assert "docker" not in report.extras


def test_an_empty_requirement_list_scores_zero_without_dividing_by_zero():
    report = _match([])

    assert report.score == 0
    assert report.outcomes == ()


def test_end_to_end_against_a_real_advert():
    ad = """Ihr Profil
- Abgeschlossenes Studium der Informatik oder vergleichbare Qualifikation
- Mindestens 2 Jahre Berufserfahrung
- Kenntnisse in C#, .NET und SQL sind zwingend erforderlich
- Erfahrung mit Docker von Vorteil
- Kenntnisse in Angular wünschenswert
"""
    profile = parse_vacancy(ad)
    report = evaluate_match(list(profile.requirements), CV, CV, today=TODAY)

    statuses = {o.requirement.key: o.status for o in report.outcomes}
    assert statuses["csharp"] == "met"
    assert statuses["angular"] == "missing"
    assert report.missing_must == ()
    assert report.score >= 80
