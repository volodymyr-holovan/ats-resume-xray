"""Ordinary sentences must not produce technologies.

There is already a test for the *inflection* path -- mongoose, excels,
swiftly -- because that is where the MongoDB-on-a-character-sheet bug came
from. Every false positive found since took the other path: an exact alias
that is also an ordinary word, which the inflection guards never see.

"Infusionen bis 500 ml" reported Machine Learning, from realistic nursing
adverts in five languages. "Daily cleaning of offices" reported Scrum.
"Chef de rang" reported Puppet -- and did so from inside this suite's own
multilingual sweep, which passed anyway because it only checked that no
*benefit* word had been picked up.

The rule for adding a spelling to AMBIGUOUS_ALIASES is the corpus, not the
dictionary: it has to appear as an ordinary word in CV and advert text.
"Angular" is an English adjective and stays, because nobody writes about
angular momentum on a CV and half the front-end adverts in Germany ask for
the framework by that exact word.
"""

import pytest

from ats_xray.skills_lexicon import ALIAS_TO_ID, SKILLS, find_skills, label_for

ORDINARY_SENTENCES = [
    ("Infusionen bis 500 ml verabreichen", "machinelearning"),
    ("Administer up to 500 ml of fluid", "machinelearning"),
    ("Preparar infusiones de hasta 500 ml", "machinelearning"),
    ("Daily cleaning of offices and stairwells", "scrum"),
    ("Safe handling of cleaning chemicals", "scrum"),
    ("Solid experience with commercial design software", "designpatterns"),
    ("Keep the rest of the workroom tidy", "rest"),
    ("Führung von Teams mit bis zu acht Personen", "m365"),
    ("Chef de rang für unser Restaurant gesucht", "puppet"),
    ("Calle San Juan 14, 28013 Madrid", "truenas"),
    ("Arbeitsort ist 4051 Basel", "risikomanagement"),
    ("Maya Bergmann, Erzieherin", "dreid"),
    ("Wer Kinder mag und geduldig ist", "schweissen"),
    ("Ansetzen von Fonds und Saucen", "anlageberatung"),
    ("Rückkehr ins Depot am Ende der Schicht", "anlageberatung"),
    ("Ein Satz Werkzeuge wird gestellt", "grafikdesign"),
    ("Die Optik der Räume muss stimmen", "physik"),
]


@pytest.mark.parametrize("sentence,forbidden", ORDINARY_SENTENCES)
def test_an_ordinary_sentence_yields_no_technology(sentence, forbidden):
    found = find_skills(sentence)

    assert forbidden not in found, (
        f"{sentence!r} was read as {label_for(forbidden)}"
    )


STILL_REACHABLE = [
    ("Erfahrung mit Machine Learning und MLOps", "machinelearning"),
    ("Scaled Agile Framework und Daily Standup", "scrum"),
    ("Kenntnis der SOLID principles", "designpatterns"),
    ("Anbindung von REST-APIs", "rest"),
    ("RESTful APIs entwickeln", "rest"),
    ("Zusammenarbeit über Microsoft Teams", "m365"),
    ("Konfigurationsmanagement mit Chef Infra", "puppet"),
    ("Betrieb von SAN Storage", "truenas"),
    ("Meldewesen nach Basel III", "risikomanagement"),
    ("Modellierung in Autodesk Maya", "dreid"),
    ("MAG-Schweißen und WIG-Schweißen", "schweissen"),
    ("Beratung zu Investmentfonds", "anlageberatung"),
    ("Schriftsatz und Reinzeichnung", "grafikdesign"),
    ("Technische Optik und Lasertechnik", "physik"),
]


@pytest.mark.parametrize("sentence,expected", STILL_REACHABLE)
def test_the_skill_is_still_reachable_by_a_longer_name(sentence, expected):
    """Blacklisting a spelling is only acceptable if the skill survives it.
    AMBIGUOUS_ALIASES says every entry stays reachable through a longer,
    unambiguous alias; this is where that claim is checked."""
    assert expected in find_skills(sentence), f"{sentence!r} no longer finds {expected}"


def test_no_alias_mixes_scripts():
    """The "reno" alias on Notariat carried a Cyrillic о. fold() preserves
    Cyrillic deliberately, so the alias could never match Latin text and a
    real ReNo-Fachangestellte advert produced nothing from it. One
    invisible character, and no test could see it."""
    mixed = []
    for skill in SKILLS:
        for alias in skill.aliases:
            letters = {"CYRILLIC" if "Ѐ" <= ch <= "ӿ" else "LATIN"
                       for ch in alias if ch.isalpha()}
            if len(letters) > 1:
                mixed.append(f"{skill.id}: {alias!r}")

    assert not mixed, "aliases mixing Latin and Cyrillic letters:\n" + "\n".join(mixed)


def test_every_ambiguous_alias_actually_exists():
    """A blacklist entry that matches no alias is dead weight that reads
    like protection."""
    from ats_xray.skills_lexicon import AMBIGUOUS_ALIASES
    from ats_xray.normalize import fold

    declared = {fold(alias) for skill in SKILLS for alias in skill.aliases}
    orphans = sorted(AMBIGUOUS_ALIASES - declared)

    assert not orphans, f"blacklisted spellings that are not aliases: {orphans}"


def test_blacklisted_spellings_are_not_reachable():
    from ats_xray.skills_lexicon import AMBIGUOUS_ALIASES

    leaked = sorted(alias for alias in AMBIGUOUS_ALIASES if alias in ALIAS_TO_ID)

    assert not leaked, f"blacklisted but still indexed: {leaked}"
