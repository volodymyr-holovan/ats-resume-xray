import pytest

from ats_xray.langid import detect_language, merge_for, vocabulary_languages

ADVERTS = {
    "de": """Ihr Profil
- Abgeschlossenes Studium der Informatik oder eine vergleichbare Qualifikation
- Kenntnisse in Python und SQL sind zwingend erforderlich
- Erfahrung mit Docker ist von Vorteil""",
    "en": """Requirements
- A completed degree in computer science or a comparable qualification
- Knowledge of Python and SQL is required
- Experience with Docker is a plus""",
    "es": """Tu perfil
- Estudios de informatica o una titulacion equivalente
- Conocimientos de Python y SQL son imprescindibles
- Experiencia con Docker es un plus""",
    "nl": """Jouw profiel
- Een afgeronde opleiding informatica of vergelijkbaar
- Kennis van Python en SQL is vereist
- Ervaring met Docker is een pre""",
    "fr": """Votre profil
- Un diplome en informatique ou une formation equivalente
- La connaissance de Python et SQL est exigee
- Une experience avec Docker est un atout""",
    "uk": """Ваш профіль
- Вища освіта з інформатики або еквівалентна кваліфікація
- Знання Python та SQL є обов'язковими
- Досвід роботи з Docker буде перевагою""",
    "ru": """Ваш профиль
- Высшее образование по информатике или эквивалентная квалификация
- Знание Python и SQL является обязательным
- Опыт работы с Docker будет преимуществом""",
}


@pytest.mark.parametrize(("expected", "text"), ADVERTS.items())
def test_every_supported_language_is_recognised(expected, text):
    assert detect_language(text) == expected


@pytest.mark.parametrize(("expected", "text"), ADVERTS.items())
def test_case_does_not_change_the_answer(expected, text):
    """Adverts arrive shouted, lower-cased and everything between."""
    assert detect_language(text.upper()) == expected
    assert detect_language(text.lower()) == expected


def test_a_terse_cv_is_still_recognised():
    """A CV is not prose. This one carries two German function words, which
    on their own had it read as English until section headings and umlauts
    were counted as evidence too."""
    cv = """Jane Doe
jane@example.com

Ausbildung
Bachelor of Science, Informatik
Technische Universitaet, 09/2021 - 06/2025

Berufserfahrung
Technischer Support, 09/2023 - 06/2026
Betrieb und Wartung von Technik

Kenntnisse
Python, SQL, Docker

Sprachen
Deutsch - B2, Englisch - C1"""

    assert detect_language(cv) == "de"


def test_ukrainian_and_russian_are_told_apart_by_their_alphabets():
    """They share most function words, so the letters each has and the other
    lacks are what decides."""
    assert detect_language("Знання та досвід роботи з системами і мережами компанії") == "uk"
    assert detect_language("Знание и опыт работы с системами и сетями компании") == "ru"


def test_english_bullets_inside_a_german_advert_do_not_flip_the_answer():
    text = ADVERTS["de"] + "\n- Experience with Kubernetes is a plus"

    assert detect_language(text) == "de"


def test_text_too_short_to_judge_falls_back_to_english():
    """English is the safe default: its vocabulary is read alongside every
    other language anyway, so falling back to it loses nothing."""
    assert detect_language("Docker SQL") == "en"
    assert detect_language("") == "en"


def test_the_reading_set_is_the_document_language_plus_english():
    assert vocabulary_languages("de") == ("de", "en")
    assert vocabulary_languages("en") == ("en",)


def test_merge_for_flattens_only_the_languages_worth_reading():
    mapping = {"de": ("a",), "en": ("b",), "fr": ("c",)}

    assert merge_for(mapping, "de") == ("a", "b")
    assert "c" not in merge_for(mapping, "de")
