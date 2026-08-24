from datetime import date

import pytest

from ats_xray.credentials import (
    education_waived,
    find_education,
    find_experience_months,
    find_languages,
    find_licence,
    find_required_years,
    language_required_without_level,
)


# --------------------------------------------------------------- education
@pytest.mark.parametrize(
    ("text", "level", "field"),
    [
        ("Abgeschlossenes Studium der Informatik", "bachelor", "informatik"),
        ("Abgeschlossene Ausbildung als Fachinformatiker", "ausbildung", "informatik"),
        ("Masterabschluss in Elektrotechnik", "master", "engineering"),
        ("Bachelor of Science, Informatik", "bachelor", "informatik"),
        ("B.Sc. Informatik", "bachelor", "informatik"),
        ("M.Sc. Data Science", "master", "mathematics"),
        ("Dipl.-Ing. Maschinenbau", "master", "engineering"),
        ("Bachelor's degree in Computer Science", "bachelor", "informatik"),
    ],
)
def test_education_level_and_field_are_read(text, level, field):
    fact = find_education(text)

    assert fact is not None
    assert (fact.level, fact.field) == (level, field)


def test_scrum_master_is_not_a_masters_degree():
    """The single most likely false positive in a German IT advert: every
    other one mentions a Scrum Master, and reading that as a degree would
    put an invented requirement on the report."""
    assert find_education("Erfahrung als Scrum Master von Vorteil") is None
    assert find_education("Product Master und Data Master Kenntnisse") is None


def test_highest_level_wins_when_several_are_named():
    """A CV lists an apprenticeship and then a degree; it has the degree."""
    fact = find_education("Abgeschlossene Ausbildung als Fachinformatiker\nMasterabschluss Informatik")

    assert fact.level == "master"


def test_equivalent_qualification_is_recorded():
    """"oder vergleichbare Qualifikation" turns a gate into a preference,
    which is the difference between a blocking gap and a note."""
    fact = find_education("Abgeschlossenes Studium der Informatik oder vergleichbare Qualifikation")

    assert fact.equivalent_accepted
    assert not find_education("Abgeschlossenes Studium der Informatik").equivalent_accepted


def test_career_changers_waive_the_requirement_entirely():
    assert education_waived("Quereinsteiger willkommen, auch ohne Studium")
    assert not education_waived("Abgeschlossenes Studium erforderlich")


# -------------------------------------------------------------- experience
@pytest.mark.parametrize(
    ("text", "years"),
    [
        ("Mindestens 3 Jahre Berufserfahrung", 3),
        ("3+ years of experience with Docker", 3),
        ("3 bis 5 Jahre Erfahrung", 3),
        ("Mehrjährige Erfahrung in der Softwareentwicklung", 3),
        ("Erste Berufserfahrung wünschenswert", 1),
    ],
)
def test_required_years_are_read(text, years):
    assert find_required_years(text) == years


def test_a_number_of_years_is_only_a_requirement_next_to_experience():
    """"2 Jahre" turns up in contract terms and project durations. Without
    the word "Erfahrung" nearby it is not a requirement."""
    assert find_required_years("Der Vertrag läuft zunächst 2 Jahre") is None
    assert find_required_years("Das Projekt dauerte 4 Jahre") is None


def test_experience_months_counts_a_single_range():
    assert find_experience_months("09/2023 - 06/2026", today=date(2026, 8, 24)) == 34


def test_overlapping_periods_are_merged_not_added():
    """Working while studying does not give someone two careers. Summing
    the spans would let a CV claim more years than the person has lived."""
    overlapping = "01/2020 - 12/2022\n01/2021 - 12/2023"

    assert find_experience_months(overlapping, today=date(2026, 8, 24)) == 48


def test_open_ended_periods_run_to_today():
    months = find_experience_months("seit 01/2026", today=date(2026, 8, 24))

    assert months == 8


def test_present_day_words_are_understood():
    months = find_experience_months("03/2026 - heute", today=date(2026, 8, 24))

    assert months == 6


# ---------------------------------------------------------------- languages
def test_level_written_after_the_language_is_read():
    facts = {f.language: f.level for f in find_languages("Deutsch - B2, Englisch - C1")}

    assert facts == {"de": "b2", "en": "c1"}


def test_level_written_before_the_language_is_read():
    """German puts the adjective first. Only looking forward from the
    language name misses every advert phrased the normal way."""
    facts = {f.language: f.level for f in find_languages(
        "Verhandlungssichere Deutschkenntnisse und gute Englischkenntnisse"
    )}

    assert facts == {"de": "c1", "en": "b2"}


def test_a_level_is_not_borrowed_from_the_neighbouring_language():
    facts = {f.language: f.level for f in find_languages(
        "Fließende Englischkenntnisse erforderlich, Deutsch von Vorteil"
    )}

    assert facts == {"en": "c1"}
    assert language_required_without_level(
        "Fließende Englischkenntnisse erforderlich, Deutsch von Vorteil"
    ) == ["de"]


def test_longer_descriptor_wins_over_the_one_inside_it():
    facts = {f.language: f.level for f in find_languages("Sehr gute Deutschkenntnisse")}

    assert facts == {"de": "c1"}


def test_native_speaker_is_c2():
    facts = {f.language: f.level for f in find_languages("Ukrainisch - Muttersprache")}

    assert facts == {"uk": "c2"}


# ------------------------------------------------------------------ licence
def test_licence_class_is_read_and_defaults_to_b():
    assert find_licence("Führerschein Klasse B erforderlich") == "B"
    assert find_licence("Fahrerlaubnis wünschenswert") == "B"
    assert find_licence("Führerschein Klasse C1") == "C1"
    assert find_licence("Keine besonderen Anforderungen") is None
