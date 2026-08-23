import pytest

from ats_xray.sections import (
    SECTION_ALIASES_BY_LANGUAGE,
    find_section_headers,
    normalize_heading,
    split_into_sections,
)


def test_find_section_headers_matches_standalone_english_headers():
    text = "Jane Doe\n\nExperience\nSenior Engineer at Acme\n\nEducation\nBSc Computer Science"
    headers = find_section_headers(text)
    assert [h["section"] for h in headers] == ["experience", "education"]


def test_find_section_headers_matches_german_headers():
    text = "Max Mustermann\n\nBerufserfahrung\nEntwickler bei Acme\n\nAusbildung\nInformatik"
    headers = find_section_headers(text)
    assert [h["section"] for h in headers] == ["experience", "education"]


def test_find_section_headers_ignores_word_inside_a_sentence():
    text = "My experience includes leading three teams over five years."
    assert find_section_headers(text) == []


def test_find_section_headers_tolerates_trailing_colon():
    text = "Skills:\nPython, SQL"
    headers = find_section_headers(text)
    assert [h["section"] for h in headers] == ["skills"]


def test_split_into_sections_assigns_content_between_headers():
    text = "Jane Doe\njane@example.com\n\nExperience\nSenior Engineer at Acme\n\nEducation\nBSc Computer Science"
    sections = split_into_sections(text)
    assert sections["preamble"] == "Jane Doe\njane@example.com"
    assert sections["experience"] == "Senior Engineer at Acme"
    assert sections["education"] == "BSc Computer Science"


def test_split_into_sections_no_headers_returns_whole_text_as_preamble():
    text = "Just some unstructured text with no recognizable headers."
    assert split_into_sections(text) == {"preamble": text}


def test_split_into_sections_merges_repeated_section_type():
    text = "Skills\nPython\n\nLanguages\nEnglish\n\nSkills\nSQL"
    sections = split_into_sections(text)
    assert sections["skills"] == "Python\nSQL"
    assert sections["languages"] == "English"


LANGUAGE_SAMPLES = {
    "uk": "Іван Петренко\n\nДосвід роботи\nSenior Developer\n\nОсвіта\nКПІ\n\nНавички\nPython",
    "ru": "Иван Петров\n\nОпыт работы\nРазработчик\n\nОбразование\nМГУ\n\nНавыки\nPython",
    "es": "Juan Pérez\n\nExperiencia laboral\nDesarrollador\n\nEducación\nUPM\n\nHabilidades\nPython",
    "nl": "Jan Jansen\n\nWerkervaring\nOntwikkelaar\n\nOpleiding\nTU Delft\n\nVaardigheden\nPython",
    "fr": "Jean Dupont\n\nExpérience professionnelle\nDéveloppeur\n\nFormation\nSorbonne\n\nCompétences\nPython",
}


@pytest.mark.parametrize("language,text", LANGUAGE_SAMPLES.items(), ids=list(LANGUAGE_SAMPLES))
def test_core_sections_are_recognized_in_each_supported_language(language, text):
    sections = split_into_sections(text)

    assert {"experience", "education", "skills"} <= set(sections)


def test_headings_are_recognized_regardless_of_case_in_cyrillic():
    """Resumes routinely set headings in caps; Unicode lowercasing has to
    handle Cyrillic, not just ASCII.
    """
    sections = split_into_sections("Іван\n\nДОСВІД РОБОТИ\nDev\n\nОСВІТА\nКПІ")

    assert {"experience", "education"} <= set(sections)


def test_headings_are_recognized_with_diacritics():
    sections = split_into_sections("Jean\n\nÉTUDES\nSorbonne\n\nCOMPÉTENCES\nPython")

    assert {"education", "skills"} <= set(sections)


def test_a_resume_mixing_languages_still_resolves():
    """Matching runs against every language at once, so an English heading
    above Ukrainian content resolves the same as a consistent document.
    """
    sections = split_into_sections("Іван\n\nExperience\nРозробник\n\nОсвіта\nКПІ")

    assert {"experience", "education"} <= set(sections)


def test_every_language_table_covers_the_scored_sections():
    """experience/education/skills drive the score, so a language missing
    one of them would silently under-report for resumes written in it.
    """
    for language, table in SECTION_ALIASES_BY_LANGUAGE.items():
        missing = {"experience", "education", "skills"} - set(table)
        assert not missing, f"{language} has no aliases for {missing}"


def test_no_alias_is_blank_or_unnormalized():
    """Aliases are compared against normalize_heading output, so any alias
    that is not already in that form could never match.
    """
    for language, table in SECTION_ALIASES_BY_LANGUAGE.items():
        for section, aliases in table.items():
            for alias in aliases:
                assert alias, f"empty alias in {language}/{section}"
                assert alias == normalize_heading(alias), f"{language}/{section}: {alias!r} is not normalized"
