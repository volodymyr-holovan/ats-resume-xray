"""Unit tests for the typed requirement vocabularies.

Most cases pass a language explicitly. A single phrase is far too short for
language detection to work on, and these tests exercise one language's
vocabulary at a time; real callers detect once over the whole document and
pass the result down.
"""

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


def _levels(text, language):
    return {f.language: f.level for f in find_languages(text, language)}


# --------------------------------------------------------------- education
@pytest.mark.parametrize(
    ("text", "language", "level", "field"),
    [
        ("Abgeschlossenes Studium der Informatik", "de", "bachelor", "informatik"),
        ("Abgeschlossene Ausbildung als Fachinformatiker", "de", "ausbildung", "informatik"),
        ("Masterabschluss in Elektrotechnik", "de", "master", "engineering"),
        ("Bachelor of Science, Informatik", "de", "bachelor", "informatik"),
        ("B.Sc. Informatik", "de", "bachelor", "informatik"),
        ("M.Sc. Data Science", "de", "master", "mathematics"),
        ("Dipl.-Ing. Maschinenbau", "de", "master", "engineering"),
        ("Bachelor's degree in Computer Science", "en", "bachelor", "informatik"),
        ("PhD in physics", "en", "doctorate", "mathematics"),
        ("Estudios de informatica", "es", "bachelor", "informatik"),
        ("Afgeronde opleiding informatica", "nl", "bachelor", "informatik"),
        ("Diplome en informatique", "fr", "bachelor", "informatik"),
        ("Вища освіта з інформатики", "uk", "bachelor", "informatik"),
        ("Высшее образование по информатике", "ru", "bachelor", "informatik"),
    ],
)
def test_education_level_and_field_are_read(text, language, level, field):
    fact = find_education(text, language)

    assert fact is not None
    assert (fact.level, fact.field) == (level, field)


def test_scrum_master_is_not_a_masters_degree():
    """The single most likely false positive in a German IT advert: every
    other one mentions a Scrum Master, and reading that as a degree would put
    an invented requirement on the report."""
    assert find_education("Erfahrung als Scrum Master von Vorteil", "de") is None
    assert find_education("Product Master und Data Master Kenntnisse", "de") is None


def test_an_abbreviation_does_not_match_inside_a_longer_word():
    """Two real failures: "m sc" was found in "zu**m sc**hichtdienst" and
    "bsc" in "A**bsc**hlussstärke", each inventing a degree out of nothing."""
    assert find_education("Bereitschaft zum Schichtdienst", "de") is None
    assert find_education("Verhandlungsgeschick und Abschlussstärke", "de") is None


def test_a_foreign_degree_word_does_not_leak_into_german():
    """Spanish "diploma" sits inside German "Diplomatie". Reading only the
    document's own language plus English is what keeps them apart."""
    assert find_education("Erfahrung in der Diplomatie", "de") is None


def test_highest_level_wins_when_several_are_named():
    """A CV lists an apprenticeship and then a degree; it has the degree."""
    fact = find_education(
        "Abgeschlossene Ausbildung als Fachinformatiker\nMasterabschluss Informatik", "de"
    )

    assert fact.level == "master"


def test_a_masters_degree_is_not_understated_as_a_bachelor():
    """"Master's degree in engineering" also contains "degree in", which on
    its own reads as a Bachelor."""
    fact = find_education("Master's degree in engineering is required", "en")

    assert fact.level == "master"


def test_equivalent_qualification_is_recorded():
    """"oder vergleichbare Qualifikation" turns a gate into a preference,
    which is the difference between a blocking gap and a note."""
    fact = find_education("Abgeschlossenes Studium der Informatik oder vergleichbare Qualifikation", "de")

    assert fact.equivalent_accepted
    assert not find_education("Abgeschlossenes Studium der Informatik", "de").equivalent_accepted


def test_career_changers_waive_the_requirement_entirely():
    assert education_waived("Quereinsteiger willkommen, auch ohne Studium", "de")
    assert not education_waived("Abgeschlossenes Studium erforderlich", "de")


# -------------------------------------------------------------- experience
@pytest.mark.parametrize(
    ("text", "language", "years"),
    [
        ("Mindestens 3 Jahre Berufserfahrung", "de", 3),
        ("3 bis 5 Jahre Erfahrung", "de", 3),
        ("Mehrjährige Erfahrung in der Softwareentwicklung", "de", 3),
        ("Erste Berufserfahrung wünschenswert", "de", 1),
        ("3+ years of experience with Docker", "en", 3),
        ("Several years of experience", "en", 3),
        ("Experiencia de 4 anos", "es", 4),
        ("Досвід роботи від 2 років", "uk", 2),
    ],
)
def test_required_years_are_read(text, language, years):
    assert find_required_years(text, language) == years


def test_a_number_of_years_is_only_a_requirement_next_to_experience():
    """"2 Jahre" turns up in contract terms and project durations. Without
    the word "Erfahrung" nearby it is not a requirement."""
    assert find_required_years("Der Vertrag läuft zunächst 2 Jahre", "de") is None
    assert find_required_years("Das Projekt dauerte 4 Jahre", "de") is None


def test_experience_months_counts_a_single_range():
    assert find_experience_months("09/2023 - 06/2026", today=date(2026, 8, 24)) == 34


def test_overlapping_periods_are_merged_not_added():
    """Working while studying does not give someone two careers. Summing the
    spans would let a CV claim more years than the person has lived."""
    overlapping = "01/2020 - 12/2022\n01/2021 - 12/2023"

    assert find_experience_months(overlapping, today=date(2026, 8, 24)) == 48


def test_open_ended_periods_run_to_today():
    assert find_experience_months("seit 01/2026", today=date(2026, 8, 24)) == 8


def test_present_day_words_are_understood():
    assert find_experience_months("03/2026 - heute", today=date(2026, 8, 24)) == 6


# ---------------------------------------------------------------- languages
def test_level_written_after_the_language_is_read():
    assert _levels("Deutsch - B2, Englisch - C1", "de") == {"de": "b2", "en": "c1"}


def test_level_written_before_the_language_is_read():
    """German puts the adjective first. Only looking forward from the
    language name misses every advert phrased the normal way."""
    levels = _levels("Verhandlungssichere Deutschkenntnisse und gute Englischkenntnisse", "de")

    assert levels == {"de": "c1", "en": "b2"}


def test_a_level_is_not_borrowed_from_the_neighbouring_language():
    text = "Fließende Englischkenntnisse erforderlich, Deutsch von Vorteil"

    assert _levels(text, "de") == {"en": "c1"}
    assert language_required_without_level(text, "de") == ["de"]


def test_longer_descriptor_wins_over_the_one_inside_it():
    assert _levels("Sehr gute Deutschkenntnisse", "de") == {"de": "c1"}


def test_native_speaker_is_c2():
    assert _levels("Ukrainisch - Muttersprache", "de") == {"uk": "c2"}


@pytest.mark.parametrize(
    ("text", "language"),
    [
        ("Aleman fluido", "es"),
        ("Vloeiend Duits", "nl"),
        ("Allemand courant", "fr"),
        ("Німецька мова на рівні C1", "uk"),
        ("Немецкий язык на уровне C1", "ru"),
        ("Fluent German", "en"),
    ],
)
def test_every_language_names_german_in_its_own_words(text, language):
    """An advert written in Spanish asks for "aleman", never for "Deutsch"."""
    assert _levels(text, language) == {"de": "c1"}


def test_a_language_named_without_a_level_is_still_reported():
    assert language_required_without_level("Wir erwarten Deutsch und Englisch", "de") == ["de", "en"]


# ------------------------------------------------------------------ licence
def test_licence_class_is_read_and_defaults_to_b():
    assert find_licence("Führerschein Klasse B erforderlich") == "B"
    assert find_licence("Fahrerlaubnis wünschenswert") == "B"
    assert find_licence("Führerschein Klasse C1") == "C1"
    assert find_licence("Keine besonderen Anforderungen") is None
