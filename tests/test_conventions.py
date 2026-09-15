"""What a CV says against the conventions of the country it is going to.

Every other test here asks whether software can read a file. These ask
whether a recruiter reading it will find what they expect, and they are held
to the same standard the rest of the project is: each check fires on the
case it exists for, stays quiet on the cases that only look like it, and
stays quiet entirely outside the languages where the research found a rule
rather than a preference.

The negative cases are the larger half on purpose. "Evangelisches
Krankenhaus" is an employer, not a confession; an FSJ is a paid placement,
not volunteering; "Phase I" is a numeral, not a pronoun. A convention check
that cannot tell those apart would be telling people to delete their jobs.
"""

from datetime import date

import pytest

import ats_xray.rules  # noqa: F401  (registers the rule set)
from ats_xray.action_plan import build_plan
from ats_xray.conventions import (
    analyze_conventions,
    find_first_person,
    find_impossible_dates,
    find_oldest_first,
    find_outdated_personal_details,
    find_unexplained_gap,
    find_volunteering_in_experience,
)
from ats_xray.credentials import find_experience_months
from ats_xray.engine import Finding
from ats_xray.rule import CONVENTION, PARSING, Rule, all_rules, get_rule
from ats_xray.score import score_resume
from ats_xray.sections import split_into_sections

TODAY = date(2026, 9, 15)


def cv(*lines: str) -> str:
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------
# Volunteering listed as employment
# --------------------------------------------------------------------------

LONG_CAREER_WITH_VOLUNTEERING = cv(
    "Anna Muster",
    "Berufserfahrung",
    "03/2019 - heute  Studio Nord, Hamburg",
    "01/2014 - 02/2019  Druckerei Alt, Bremen",
    "2016 - 2020  Tafel Hamburg e.V.",
    "Ehrenamtliche Helferin bei der Lebensmittelausgabe",
    "Ausbildung",
    "2011 - 2014  HAW Hamburg",
)


def test_volunteering_under_work_experience_is_reported_in_a_german_cv():
    found = find_volunteering_in_experience(LONG_CAREER_WITH_VOLUNTEERING, "de")

    assert found is not None
    assert found.severity == "medium"
    assert "Ehrenamtliche Helferin" in found.params["text"]


def test_a_career_starter_is_told_the_exception_exists():
    """German guidance lets someone with little experience list relevant
    volunteering as practice. The finding still appears -- the convention is
    worth knowing -- but at the lower level and with its own wording."""
    starter = cv(
        "Lena Neu",
        "Berufserfahrung",
        "09/2025 - heute  Werkstudentin, Firma X",
        "2023 - 2025  Ehrenamtliche Trainerin, TSV Bremen",
        "Ausbildung",
        "2021 - 2025  Universität Bremen",
    )

    found = find_volunteering_in_experience(starter, "de")

    assert found.severity == "low"
    assert found.evidence_key == "evidence_volunteering_starter"


@pytest.mark.parametrize(
    "service",
    [
        "Freiwilliges Soziales Jahr, Kita Sonnenschein",
        "Freiwilliges Ökologisches Jahr, NABU",
        "Bundesfreiwilligendienst, Klinikum Nord",
        "FSJ im Pflegeheim am Park",
        "Freiwilliger Wehrdienst, Bundeswehr",
    ],
)
def test_a_formal_voluntary_service_is_left_under_experience(service):
    """These carry the word "freiwillig" and are paid, insured, full-time
    placements that German guidance places under Berufserfahrung. Flagging
    one would tell a school leaver to move the only real work they have."""
    text = cv("Max Muster", "Berufserfahrung", f"09/2024 - 08/2025  {service}")

    assert find_volunteering_in_experience(text, "de") is None


def test_volunteering_in_its_own_section_is_what_the_convention_asks_for():
    text = cv(
        "Clara Klar",
        "Berufserfahrung",
        "04/2021 - heute  Senior Entwicklerin, Firma Y",
        "Ehrenamtliches Engagement",
        "2018 - heute  Ehrenamtliche Code-Club-Trainerin",
    )

    assert find_volunteering_in_experience(text, "de") is None


def test_ukrainian_cv_follows_the_same_rule():
    text = cv(
        "Олена Коваль",
        "Досвід роботи",
        "03/2020 - дотепер  Бухгалтерка, ТОВ Альфа",
        "2022 - 2024  Волонтерка, благодійний фонд",
    )

    found = find_volunteering_in_experience(text, "uk")

    assert found is not None and "Волонтерка" in found.params["text"]


@pytest.mark.parametrize(
    ("language", "heading", "entry"),
    [
        ("nl", "Werkervaring", "2016 - 2019  Vrijwilligerswerk bij het Rode Kruis"),
        ("es", "Experiencia laboral", "2016 - 2019  Voluntaria en Cruz Roja"),
        ("fr", "Expérience professionnelle", "2016 - 2019  Bénévole à la Croix-Rouge"),
        ("en", "Experience", "2016 - 2019  Volunteer, Red Cross"),
        ("ru", "Опыт работы", "2016 - 2019  Волонтер, Красный Крест"),
    ],
)
def test_countries_that_accept_volunteering_as_experience_are_left_alone(language, heading, entry):
    """Dutch, Spanish, French, English and Russian guidance all accept
    volunteering under work experience when it is relevant. Exporting the
    German rule there would be wrong advice with a citation attached."""
    text = cv("Name", heading, "2019 - 2025  Company", entry)

    assert find_volunteering_in_experience(text, language) is None


# --------------------------------------------------------------------------
# Gaps nobody explained
# --------------------------------------------------------------------------


def test_a_year_between_jobs_is_a_medium_gap():
    text = cv(
        "Petra Beispiel",
        "Berufserfahrung",
        "01/2017 - 06/2020  Klinikum Köln",
        "07/2021 - heute  Uniklinik Bonn",
    )

    found = find_unexplained_gap(text, "de", TODAY)

    assert found.severity == "medium"
    assert (found.params["start"], found.params["end"], found.params["months"]) == ("07/2020", "06/2021", 12)


def test_five_months_is_a_low_gap_and_three_is_none():
    five = cv("P", "Berufserfahrung", "01/2018 - 06/2020  A", "12/2020 - heute  B")
    three = cv("P", "Berufserfahrung", "01/2018 - 06/2020  A", "10/2020 - heute  B")

    assert find_unexplained_gap(five, "de", TODAY).severity == "low"
    assert find_unexplained_gap(three, "de", TODAY) is None


def test_every_gap_is_counted_not_only_the_longest():
    """The evidence names the longest; fixing only that one and leaving two
    more is what the reader would otherwise do."""
    text = cv(
        "P",
        "Berufserfahrung",
        "01/2012 - 12/2015  A",
        "01/2017 - 06/2020  B",
        "03/2021 - heute  C",
    )

    assert find_unexplained_gap(text, "de", TODAY).params["count"] == 2


def test_the_job_search_after_a_degree_is_allowed_for():
    """About six months of looking for a first job is normal in German
    guidance, and it is taken off the front of a gap that follows
    education."""
    text = cv(
        "P",
        "Berufserfahrung",
        "02/2022 - heute  Firma X",
        "Ausbildung",
        "10/2017 - 09/2021  Universität Köln",
    )

    assert find_unexplained_gap(text, "de", TODAY) is None


def test_overlapping_entries_leave_no_gap():
    text = cv(
        "P",
        "Berufserfahrung",
        "01/2015 - 12/2019  Hauptstelle",
        "06/2019 - 08/2021  Nebentätigkeit",
        "09/2021 - heute  Neue Stelle",
    )

    assert find_unexplained_gap(text, "de", TODAY) is None


def test_a_dated_course_fills_the_gap_it_sits_in():
    """Any dated entry covers its months, wherever it is listed. A language
    course in Weiterbildung is the explanation the convention asks for."""
    text = cv(
        "P",
        "Berufserfahrung",
        "01/2016 - 06/2020  A",
        "07/2021 - heute  B",
        "Weiterbildung",
        "07/2020 - 06/2021  Deutschkurs C1, Goethe-Institut",
    )

    assert find_unexplained_gap(text, "de", TODAY) is None


def test_time_since_the_last_job_ended_counts_too():
    """The ordinary case for the people this tool is for: the CV of someone
    looking for work, whose last entry ended a while ago."""
    text = cv("P", "Berufserfahrung", "01/2018 - 12/2024  Firma X", "01/2014 - 12/2017  Firma Y")

    found = find_unexplained_gap(text, "de", TODAY)

    assert found.params["end"] == "09/2026"


def test_a_broken_date_holds_the_gap_check_back_until_it_is_fixed():
    """One mistyped digit, one finding. Leaving the impossible range out of
    the timeline opens a hole exactly where that job was, and a real CV came
    back with a sixty-nine-month gap reported beside the date error that
    caused it. The date is the thing to fix; the gaps can only be judged
    once it is."""
    text = cv(
        "P",
        "Berufserfahrung",
        "01/2017 - 06/2020  Klinikum Köln",
        "03/2021 - 01/2020  Uniklinik Bonn",
    )

    assert find_impossible_dates(text, TODAY) is not None
    assert find_unexplained_gap(text, "de", TODAY) is None


def test_gaps_are_only_a_german_convention():
    text = cv("P", "Experience", "01/2017 - 06/2020  A", "07/2021 - present  B")

    assert find_unexplained_gap(text, "en", TODAY) is None


# --------------------------------------------------------------------------
# Dates that cannot be true
# --------------------------------------------------------------------------


@pytest.mark.parametrize("language_cv", [
    cv("John Doe", "Experience", "03/2022 - 01/2021  Acme Corp"),
    cv("Олена", "Досвід роботи", "03/2022 - 01/2021  Альфа"),
    cv("Anna", "Berufserfahrung", "März 2022 - Januar 2021  Firma"),
])
def test_a_range_that_ends_before_it_starts_is_reported_in_any_language(language_cv):
    found = find_impossible_dates(language_cv, TODAY)

    assert found.evidence_key == "evidence_date_backwards"
    assert found.severity == "medium"


def test_a_year_typed_decades_ahead_is_reported():
    text = cv("P", "Experience", "03/2025 - 03/2052  Acme Corp")

    assert find_impossible_dates(text, TODAY).evidence_key == "evidence_date_future"


def test_a_contract_ending_next_year_is_ordinary():
    text = cv("P", "Berufserfahrung", "01/2026 - 12/2027  Befristete Stelle")

    assert find_impossible_dates(text, TODAY) is None


def test_an_expected_graduation_years_away_is_how_students_write_it():
    text = cv("P", "Ausbildung", "10/2025 - 09/2030  Studium Medizin, voraussichtlich")

    assert find_impossible_dates(text, TODAY) is None


def test_a_backwards_range_already_adds_no_experience():
    """The reason this is medium rather than low: the experience it was
    written to prove is already not being counted, here as in an applicant
    tracking system."""
    assert find_experience_months("03/2022 - 01/2021", today=TODAY) == 0


# --------------------------------------------------------------------------
# Sentences about "I"
# --------------------------------------------------------------------------


def test_ich_saetze_under_experience_are_reported():
    text = cv(
        "P",
        "Berufserfahrung",
        "01/2017 - heute  Klinikum",
        "Ich habe die Station geleitet und ich war für Dienstpläne zuständig.",
    )

    found = find_first_person(text, "de")

    assert found.severity == "low" and found.params["count"] == 2


def test_the_profile_at_the_top_may_be_written_in_the_first_person():
    """Both German and US guidance make this exception, so the check does
    not look in the lines under the name or in a section labelled as a
    profile."""
    text = cv(
        "Petra Beispiel",
        "Ich bin Pflegefachkraft und ich arbeite gern im Team.",
        "Kurzprofil",
        "Ich bringe zehn Jahre Erfahrung mit, ich lerne schnell.",
        "Berufserfahrung",
        "01/2017 - heute  Stationsleitung, Klinikum",
    )

    assert find_first_person(text, "de") is None


def test_ich_gcp_is_a_standard_not_a_pronoun():
    text = cv(
        "P",
        "Berufserfahrung",
        "01/2020 - heute  Studienkoordination nach ICH-GCP",
        "Monitoring gemäß ICH-GCP und ICH E6",
    )

    assert find_first_person(text, "de") is None


def test_english_first_person_is_counted_and_roman_numerals_are_not():
    text = cv(
        "Jane Roe",
        "Experience",
        "2020 - present  Pharma Inc",
        "Led Phase I and II trials. Level I certification holder.",
        "I managed a team of five and I built the reporting pipeline.",
    )

    found = find_first_person(text, "en")

    assert found.params["count"] == 2
    assert "Phase" not in found.params["text"]


def test_first_person_is_not_checked_where_it_was_not_researched():
    text = cv("P", "Досвід роботи", "2020 - дотепер  Альфа", "Я керувала командою, я вела звіти.")

    assert find_first_person(text, "uk") is None


# --------------------------------------------------------------------------
# Personal details the law made unnecessary
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("line", "label"),
    [
        ("Familienstand: verheiratet", "Familienstand"),
        ("Konfession: evangelisch", "Konfession"),
        ("Religion: römisch-katholisch", "Religion"),
        ("Kinder: 2", "Kinder"),
        ("Name des Vaters: Klaus Muster", "Eltern"),
        ("Familienstand      ledig", "Familienstand"),
        ("Familienstand", "Familienstand"),
    ],
)
def test_an_outdated_personal_detail_is_reported(line, label):
    found = find_outdated_personal_details(cv("Anna Muster", line, "Berufserfahrung"), "de")

    assert found is not None and label in found.params["text"]
    assert found.severity == "low"


@pytest.mark.parametrize(
    "line",
    [
        "01/2012 - 12/2015  Evangelisches Krankenhaus Bremen",
        "01/2017 - 06/2020  Katholisches Klinikum Köln",
        "Religion und Ethik (Lehramt), Gymnasium",
        "Kinder- und Jugendhilfe, Jugendamt Bremen",
        "Mutter-Kind-Station, Uniklinik Bonn",
        "Kinderbetreuung in der Krippengruppe",
    ],
)
def test_the_same_words_as_an_employer_or_a_field_are_not_personal_details(line):
    """What is outdated is the personal-data field, recognisable by being a
    label. The words themselves are employers, subjects, fields and wards."""
    assert find_outdated_personal_details(cv("Anna Muster", "Berufserfahrung", line), "de") is None


def test_personal_details_are_a_german_convention():
    assert find_outdated_personal_details(cv("John", "Marital status: married"), "en") is None


# --------------------------------------------------------------------------
# Oldest entry first
# --------------------------------------------------------------------------


def test_three_jobs_running_upwards_are_reported():
    text = cv(
        "P",
        "Berufserfahrung",
        "01/2012 - 12/2015  A",
        "01/2016 - 06/2020  B",
        "07/2020 - heute  C",
    )

    found = find_oldest_first(text, "de")

    assert found.severity == "low"
    assert found.params == {"first": "01/2012 - 12/2015", "last": "07/2020 - heute"}


def test_the_expected_order_is_left_alone():
    text = cv("P", "Berufserfahrung", "07/2020 - heute  C", "01/2016 - 06/2020  B", "01/2012 - 12/2015  A")

    assert find_oldest_first(text, "de") is None


def test_two_jobs_are_not_enough_to_call_it_an_order():
    text = cv("P", "Berufserfahrung", "01/2016 - 06/2020  B", "07/2020 - heute  C")

    assert find_oldest_first(text, "de") is None


def test_one_entry_out_of_place_in_an_otherwise_newest_first_list_is_not_reported():
    text = cv(
        "P",
        "Berufserfahrung",
        "07/2020 - heute  C",
        "01/2016 - 06/2020  B",
        "03/2018 - 12/2019  Nebenjob",
        "01/2012 - 12/2015  A",
    )

    assert find_oldest_first(text, "de") is None


# --------------------------------------------------------------------------
# How the findings reach the rest of the tool
# --------------------------------------------------------------------------


def test_every_convention_rule_is_registered_as_a_convention():
    convention_ids = set(analyze_conventions("", TODAY, "de"))
    registered = {rule.id for rule in all_rules() if rule.category == CONVENTION}

    assert convention_ids == registered


def test_a_rule_with_an_unknown_category_is_refused():
    with pytest.raises(ValueError):
        Rule(id="x", description="x", severity="low", source="x", category="style")


def _fields(email=True, phone=True, sections=("experience", "education", "skills")):
    report = {
        "email": {"found": email},
        "phone": {"found": phone},
        "sections": {name: {"found": name in sections} for name in ("experience", "education", "skills")},
    }
    return report


def test_a_convention_finding_does_not_move_the_score():
    """The score measures whether the file can be read. A CV that breaks a
    German custom and parses perfectly must score like one that parses
    perfectly."""
    fields = _fields()
    convention = [
        Finding(rule=get_rule("volunteering_listed_as_employment"), evidence_key="evidence_volunteering",
                evidence_params={"text": "x"}),
        Finding(rule=get_rule("unexplained_gap"), evidence_key="evidence_gap",
                evidence_params={"count": 1, "start": "01/2020", "end": "12/2020", "months": 12}),
        Finding(rule=get_rule("impossible_dates"), evidence_key="evidence_date_backwards",
                evidence_params={"text": "x"}),
    ]

    assert score_resume(fields, fields, convention).total == score_resume(fields, fields, []).total


def test_the_plan_puts_parsing_problems_before_conventions():
    """A medium convention finding must not jump a lower parsing one: the
    parsing finding decides whether anything is read at all."""
    parsing = Finding(rule=get_rule("pdf_non_embedded_font"), evidence_key="evidence_fonts",
                      evidence_params={"fonts": "x"}, severity_override="low")
    convention = Finding(rule=get_rule("volunteering_listed_as_employment"),
                         evidence_key="evidence_volunteering", evidence_params={"text": "x"})

    steps = build_plan([convention, parsing])

    assert [step.rule_id for step in steps] == ["pdf_non_embedded_font", "volunteering_listed_as_employment"]
    assert get_rule("pdf_non_embedded_font").category == PARSING


@pytest.mark.parametrize(
    "heading",
    ["Ehrenamtliches Engagement", "Volunteering", "Волонтерство", "Волонтерская деятельность",
     "Voluntariado", "Vrijwilligerswerk", "Bénévolat"],
)
def test_a_volunteering_heading_opens_its_own_section(heading):
    """Before this, the heading was not recognised, so everything under it
    was appended to whatever section came before -- usually experience. That
    both hid the convention and counted the volunteering as years of
    professional experience against an advert."""
    text = cv("Name", "Berufserfahrung", "2019 - 2025  Company", heading, "2012 - 2018  Community")

    sections = split_into_sections(text)

    assert "2012 - 2018" in sections.get("volunteering", "")
    assert "2012 - 2018" not in sections.get("experience", "")


def test_the_engine_detects_the_language_itself():
    from ats_xray.engine import evaluate

    fields = _fields()
    findings = evaluate(
        "pdf",
        {"non_embedded_fonts": [], "repeated_header_footer_lines": [], "textless_images": []},
        fields,
        fields,
        LONG_CAREER_WITH_VOLUNTEERING,
        today=TODAY,
    )

    assert "volunteering_listed_as_employment" in {f.rule.id for f in findings}
