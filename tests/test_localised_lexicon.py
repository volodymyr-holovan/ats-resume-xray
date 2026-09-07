"""The gazetteer in the other five languages, and the fence around it.

Two things are asserted here and they pull against each other. A Spanish
advert for a waiter and a Dutch one for a service engineer have to produce
known skills rather than a page of guesses, which means the names have to
be in the table. And a name that means one thing in French must not be read
out of an English sentence, which means the table cannot be one table.
"""

import pytest

from ats_xray.normalize import fold
from ats_xray.skills_data import LOCALISED_ALIASES
from ats_xray.skills_lexicon import (
    ALIAS_TO_ID,
    LOCALISED_ALIAS_TO_ID,
    SKILLS_BY_ID,
    SLAVIC_LANGUAGES,
    _slavic_forms,
    find_skills,
)

LANGUAGES = sorted(LOCALISED_ALIASES)


@pytest.mark.parametrize("language", LANGUAGES)
def test_every_localised_row_points_at_a_skill_that_exists(language):
    """A row naming a skill id that was renamed or dropped is silently dead:
    it costs nothing at import and the language quietly loses a word."""
    unknown = sorted({row[0] for row in LOCALISED_ALIASES[language]} - set(SKILLS_BY_ID))

    assert not unknown, f"{language} names skills that do not exist: {unknown}"


@pytest.mark.parametrize(
    ("text", "language", "expected"),
    [
        ("Atencion al cliente en sala y cobro en caja", "es", {"kundenberatung", "kasse"}),
        ("Ervaring met lassen en hydrauliek", "nl", {"schweissen", "hydraulik"}),
        ("Saisie comptable et travail en equipe", "fr", {"buchhaltung", "teamfaehigkeit"}),
        ("Догляд за пацієнтами та перша допомога", "uk", {"pflege", "erstehilfe"}),
        ("Уборка помещений и работа в команде", "ru", {"reinigung", "teamfaehigkeit"}),
    ],
)
def test_an_advert_in_its_own_language_finds_known_skills(text, language, expected):
    assert expected <= set(find_skills(text, language))


def test_a_french_name_is_not_read_out_of_an_english_sentence():
    """The collision that made the table per language in the first place.
    "production" is the French for the manufacturing skill and an ordinary
    English word: a DevOps advert asking for four years of Linux in
    production was reported as needing factory experience."""
    english = "At least 4 years of experience with Linux in production"

    assert "produktion" not in find_skills(english, "en")
    assert "produktion" in find_skills("Ligne de production automatisee", "fr")


@pytest.mark.parametrize("language", LANGUAGES)
def test_a_localised_name_never_shadows_the_base_table(language):
    """The labels, the tests and the rule names are written in the German
    and English spellings. A localised name that happens to collide with one
    of them has to lose, or the same word would mean different things
    depending on what language the document was detected as."""
    shadowed = [
        fold(name)
        for row in LOCALISED_ALIASES[language]
        for name in row[1:]
        if fold(name) in ALIAS_TO_ID and LOCALISED_ALIAS_TO_ID[language].get(fold(name))
    ]

    assert not shadowed, f"{language} overrides the base table for: {shadowed}"


@pytest.mark.parametrize("language", sorted(SLAVIC_LANGUAGES))
def test_a_slavic_name_is_found_in_the_cases_an_advert_writes_it_in(language):
    """Nobody writes the nominative. "Опыт работы на складе" is where the
    warehouse is, and "склад" never appears in the sentence at all."""
    inflected = {
        "uk": ("Досвід роботи на складі", "lager"),
        "ru": ("Опыт работы на складе", "lager"),
    }[language]

    assert inflected[1] in find_skills(inflected[0], language)


@pytest.mark.parametrize("language", sorted(SLAVIC_LANGUAGES))
def test_no_two_skills_decline_into_the_same_word(language):
    """The risk this rule takes.

    Cutting a name back to its stem and adding twenty-six endings makes
    around twelve forms for every word written, and two skills whose stems
    are close enough would start producing each other's. Whichever was
    declared first would silently win, and a Ukrainian CV would match an
    advert on a skill neither document names. Two thousand forms per
    language and none of them is claimed twice; a new row that breaks that
    has to be spelled differently.
    """
    owners: dict[str, set[str]] = {}
    for row in LOCALISED_ALIASES[language]:
        for name in row[1:]:
            for form in _slavic_forms(fold(name)):
                owners.setdefault(form, set()).add(row[0])

    clashes = {form: sorted(ids) for form, ids in owners.items() if len(ids) > 1}

    assert not clashes, f"{language}: {len(clashes)} forms belong to two skills"


@pytest.mark.parametrize("language", sorted(SLAVIC_LANGUAGES))
def test_a_written_name_always_beats_a_generated_one(language):
    """The forms are generated in a second pass for exactly this reason: a
    spelling somebody wrote down is evidence, and a spelling this module
    invented is a guess."""
    table = LOCALISED_ALIAS_TO_ID[language]

    wrong = [
        (fold(name), table.get(fold(name)), row[0])
        for row in LOCALISED_ALIASES[language]
        for name in row[1:]
        if fold(name) in table and table[fold(name)] != row[0]
    ]

    assert not wrong, f"{language}: written names overruled {wrong[:5]}"
