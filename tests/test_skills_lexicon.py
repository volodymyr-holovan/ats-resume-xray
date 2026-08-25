import pytest

from ats_xray.normalize import fold
from ats_xray.skills_lexicon import (
    ALIAS_TO_ID,
    AMBIGUOUS_ALIASES,
    SKILLS,
    SKILLS_BY_ID,
    find_skills,
    label_for,
)


def test_every_skill_id_is_unique():
    ids = [skill.id for skill in SKILLS]

    assert len(ids) == len(set(ids))


def test_no_alias_folds_to_the_empty_string():
    """An empty alias would match every text. This is the same class of bug
    that made every advert heading match every line."""
    assert "" not in ALIAS_TO_ID


def test_the_label_is_always_findable_as_its_own_alias():
    """Except for the handful whose real name is an ordinary word: those
    are deliberately unreachable by their label and carry an unambiguous
    alias instead."""
    for skill in SKILLS:
        if fold(skill.label) in AMBIGUOUS_ALIASES:
            continue
        assert find_skills(skill.label) == [skill.id], skill.label


def test_the_ambiguous_ones_are_still_reachable_by_another_alias():
    for skill in SKILLS:
        if fold(skill.label) not in AMBIGUOUS_ALIASES:
            continue
        reachable = [a for a in skill.aliases if fold(a) not in AMBIGUOUS_ALIASES]
        assert reachable, f"{skill.id} has no usable alias left"
        assert find_skills(reachable[0]) == [skill.id]


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Kenntnisse in Python", "python"),
        ("Erfahrung mit Docker", "docker"),
        ("C# und .NET", "csharp"),
        ("Maschinelles Lernen", "machinelearning"),
        ("Objektorientierte Programmierung", "oop"),
        ("Versionsverwaltung mit Git", "git"),
        ("Qualitätssicherung und Testautomatisierung", "testing"),
        ("Active Directory administrieren", "activedirectory"),
    ],
)
def test_german_spellings_resolve_to_the_same_skill(text, expected):
    assert expected in find_skills(text)


def test_the_longest_alias_wins():
    """"Microsoft SQL Server" is one product. Matching the shorter "SQL"
    first would report two skills where the advert named one."""
    found = find_skills("Erfahrung mit Microsoft SQL Server")

    assert found == ["mssql"]


def test_a_mention_is_only_counted_once():
    assert find_skills("Docker, Docker und nochmal Docker") == ["docker"]


def test_ambiguous_short_names_are_left_out_of_the_lexicon():
    """"Go" and "R" are real languages whose names collide with ordinary
    words. They are reachable through unambiguous spellings instead, so an
    advert saying "go live" does not add Go to the requirements."""
    assert find_skills("Wir gehen go live und r&d") == []
    assert "golang" in find_skills("Erfahrung mit Golang")


def test_label_for_falls_back_to_the_id_for_unknown_skills():
    assert label_for("docker") == "Docker"
    assert label_for("custom:something") == "custom:something"


def test_every_registered_skill_has_a_category():
    assert all(SKILLS_BY_ID[skill.id].category for skill in SKILLS)


ORDINARY_WORDS = [
    ("mongoose", "mongodb"),
    ("mongols", "mongodb"),
    ("excels", "excel"),
    ("excelled", "excel"),
    ("swiftly", "swift"),
    ("scalar", "scala"),
    ("batches", "batch"),
    ("fluttering", "flutter"),
    ("reacts", "react"),
    ("reacted", "react"),
    ("sparks", "spark"),
    ("sparked", "spark"),
]


@pytest.mark.parametrize(("word", "was_matched_as"), ORDINARY_WORDS)
def test_an_ordinary_word_is_not_a_technology(word, was_matched_as):
    """Every one of these was observed matching a product name through the
    shared-stem comparison, which is right for German nouns and disastrous
    for names that do not inflect. "MongoDB" was reported from a blank
    character sheet this way."""
    assert find_skills(word) == [], f"{word} still reads as {was_matched_as}"


GERMAN_INFLECTIONS = [
    ("Reinigungsmitteln", "reinigungsmittel"),
    ("Pflegedokumentationen", "pflegedoku"),
    ("Reinigungsmaschinen", "reinigungsmaschinen"),
    ("Netzwerken", "networking"),
]


@pytest.mark.parametrize(("word", "skill_id"), GERMAN_INFLECTIONS)
def test_a_declined_german_noun_still_matches(word, skill_id):
    """The tolerance that had to survive: German adverts decline their
    nouns, and a dative plural is the same requirement."""
    assert skill_id in find_skills(word)


TECHNOLOGIES = [
    "MongoDB", "Excel", "Swift", "Scala", "React", "Apache Spark", "Flutter",
    "Docker", "Kubernetes", "Microsoft SQL Server", "Node.js", "C#", "PostgreSQL",
]


@pytest.mark.parametrize("name", TECHNOLOGIES)
def test_the_real_name_still_matches(name):
    assert find_skills(name), f"{name} no longer recognised"
