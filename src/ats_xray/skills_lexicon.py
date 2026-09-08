"""Recognising the skills a job advert names.

The vocabulary lives in :mod:`skills_data`; this module turns it into an
index and searches text with it.

A curated gazetteer beats free-text extraction because it is accountable: a
term is a skill because somebody put it on the list, not because it happened
to be capitalised. What the gazetteer cannot cover is handled separately in
:mod:`terms`, which guesses and says so.

Matching is longest-alias-first, so "Microsoft SQL Server" is recognised as
one product rather than as SQL plus two stray words, and case- and
umlaut-insensitive because :func:`normalize.fold` runs over both sides.
"""

from dataclasses import dataclass

from .normalize import fold
from .skills_data import ALL_SKILLS, LOCALISED_ALIASES


@dataclass(frozen=True)
class Skill:
    id: str
    label: str
    category: str
    aliases: tuple[str, ...]


def _build(row: tuple[str, ...]) -> Skill:
    id_, label, category, *aliases = row
    # The label is always an alias: the canonical spelling is the one most
    # likely to appear, and repeating it in every row would be noise.
    return Skill(id_, label, category, (label, *aliases))


SKILLS: tuple[Skill, ...] = tuple(_build(row) for row in ALL_SKILLS)
SKILLS_BY_ID: dict[str, Skill] = {skill.id: skill for skill in SKILLS}

AMBIGUOUS_ALIASES = frozenset({
    "go", "r", "c", "ad", "ai", "ki", "qa", "hr", "au", "hu", "bar", "din", "iso",
    "sap fi", "sap co",
    # Units and ordinary words that a curated list is supposed to keep out
    # and did not. Every one below was reported from a real sentence:
    "ml",       # "Infusionen bis 500 ml" -- Machine Learning, in five languages
    "safe",     # "safe handling of chemicals" -- Scrum
    "daily",    # "daily cleaning of offices" -- Scrum
    "solid",    # "solid experience with..." -- Design Patterns
    "rest",     # "keep the rest of the workroom tidy" -- REST
    "teams",    # "Führung von Teams" -- Microsoft 365
    "chef",     # "Chef de rang" -- Puppet
    "san",      # "Calle San Juan 14" -- TrueNAS
    "basel",    # "4051 Basel" -- Risikomanagement
    "maya",     # a given name on line 1 -- 3D-Modellierung
    "mag",      # "wer Kinder mag", and the Austrian Mag. title -- Schweißen
    "fonds",    # "Ansetzen von Fonds und Saucen" -- Anlageberatung
    "depot",    # a bus depot -- Anlageberatung
    "satz",     # "ein Satz Werkzeuge", "Steuersatz" -- Grafikdesign
    "optik",    # German for appearance -- Physik
    "container",  # "Be- und Entladen von Containern" -- Docker
})
"""Spellings that are never treated as a skill mention even though they are
the real name of one.

"Go live", "R&D", "a.i.", "ad hoc", "HR" inside a German sentence, "Bar" as
a place rather than the craft: each is an ordinary word somewhere, and a
requirements list that gained a programming language from a launch date
would be wrong in a way the reader cannot easily spot. Every skill here
stays reachable through a longer, unambiguous alias.

The test for this list is the corpus, not the dictionary. "Angular" is an
ordinary English adjective and belongs here by that measure -- but nobody
writes about angular momentum on a CV, and half the front-end adverts in
Germany ask for the framework by that exact word. It stays.
"""

ALIAS_TO_ID: dict[str, str] = {}
for _skill in SKILLS:
    for _alias in _skill.aliases:
        _folded = fold(_alias)
        if not _folded or _folded in AMBIGUOUS_ALIASES:
            continue
        # First writer wins: an alias listed under two skills belongs to the
        # one that declared it first, and a silent reassignment here would be
        # very hard to notice later.
        ALIAS_TO_ID.setdefault(_folded, _skill.id)

LOCALISED_ALIAS_TO_ID: dict[str, dict[str, str]] = {}
for _language, _rows in LOCALISED_ALIASES.items():
    _table: dict[str, str] = {}
    for _skill_id, *_names in _rows:
        for _name in _names:
            _folded = fold(_name)
            if not _folded or _folded in AMBIGUOUS_ALIASES or _folded in ALIAS_TO_ID:
                continue
            _table.setdefault(_folded, _skill_id)
    LOCALISED_ALIAS_TO_ID[_language] = _table
"""What each skill is called in the other five languages, kept per language.

One flat table was fine while it held German and English. It stopped being
fine the moment the other five went in: French "production" met an English
sentence about four years of Linux "in production" and reported the
manufacturing skill, and "service", "animation", "formation" and
"administration" are all waiting to do the same. So a document is read
against its own language and the base table, never against all seven --
which is the rule ``langid`` already applies to every other vocabulary
here.

A name the base table already claims is dropped rather than allowed to
shadow it: the German and English spellings are the ones the labels and the
tests are written in."""

SLAVIC_LANGUAGES = frozenset({"uk", "ru"})
SLAVIC_CASE_ENDINGS = (
    "", "а", "и", "і", "у", "е", "о", "я", "ю", "ы", "ой", "ей", "ом", "ем",
    "ою", "ев", "ов", "ів", "ам", "ям", "ах", "ях", "ами", "ями", "ії", "ия",
)
MIN_SLAVIC_STEM = 5
_SLAVIC_FINAL_VOWELS = "аеиійоуыьэюя"
"""Ukrainian and Russian decline the noun rather than adding to it.

The German rule -- alias plus one of nine endings -- does not reach a single
Slavic form: "каса" becomes "касі", "склад" becomes "складі", "прибирання"
becomes "прибиранням". The ending replaces the last vowel instead of
following it, so the stem has to be cut back one character before the
endings go on.

The five-character floor on the stem is what keeps this from turning into a
prefix match. It is the same reasoning as :data:`MIN_INFLECTED_ALIAS`, and
it matters more here because there are more endings to collide through."""


def _slavic_forms(alias: str) -> tuple[str, ...]:
    """Every case form of a single-word Slavic alias, or nothing.

    Multi-word aliases are left alone: declining each word independently
    produces phrases nobody writes, and the phrase itself is usually the
    fixed expression an advert uses.
    """
    if " " in alias:
        return ()
    stem = alias[:-1] if alias[-1:] in _SLAVIC_FINAL_VOWELS else alias
    if len(stem) < MIN_SLAVIC_STEM:
        return ()
    return tuple(stem + ending for ending in SLAVIC_CASE_ENDINGS)


for _language in SLAVIC_LANGUAGES & set(LOCALISED_ALIAS_TO_ID):
    _table = LOCALISED_ALIAS_TO_ID[_language]
    # Second pass on purpose: every spelling somebody actually wrote is
    # already in the table, so a generated form can never displace one.
    for _alias, _skill_id in list(_table.items()):
        for _form in _slavic_forms(_alias):
            if _form not in ALIAS_TO_ID:
                _table.setdefault(_form, _skill_id)

MAX_ALIAS_WORDS = max(
    len(alias.split())
    for table in (ALIAS_TO_ID, *LOCALISED_ALIAS_TO_ID.values())
    for alias in table
)

_SINGLE_WORD_ALIASES: dict[str, str] = {
    alias: skill_id for alias, skill_id in ALIAS_TO_ID.items() if " " not in alias
}


def label_for(skill_id: str) -> str:
    skill = SKILLS_BY_ID.get(skill_id)
    return skill.label if skill else skill_id


def find_skills(text: str, language: str | None = None) -> list[str]:
    """Skill ids mentioned in ``text``, in order of first appearance."""
    return find_skills_and_covered(text, language)[0]


def find_skills_and_covered(
    text: str, language: str | None = None
) -> tuple[list[str], set[str]]:
    """Skill ids plus the folded words those matches used up.

    The second half exists for the generic term extractor: a word already
    explained by a lexicon hit must not come back as a separate keyword, or
    "Microsoft SQL Server" would be reported once as a skill and three more
    times as loose nouns.

    ``language`` opens that language's names in addition to the base table.
    Left out, only the base table is read, which is the right default for a
    caller that does not know what it is holding.
    """
    words = fold(text).split() if text else []
    consumed = [False] * len(words)
    found: list[str] = []
    localised = LOCALISED_ALIAS_TO_ID.get(language or "", _NO_ALIASES)

    for size in range(min(MAX_ALIAS_WORDS, len(words)), 0, -1):
        for start in range(len(words) - size + 1):
            if any(consumed[start : start + size]):
                continue
            skill_id = _lookup(words[start : start + size], localised)
            if skill_id is None:
                continue
            for index in range(start, start + size):
                consumed[index] = True
            if skill_id not in found:
                found.append(skill_id)

    covered = {word for word, used in zip(words, consumed) if used}
    return found, covered


_NO_ALIASES: dict[str, str] = {}


MIN_INFLECTED_ALIAS = 8
"""Shortest alias allowed to match an inflected form of itself.

The general shared-stem comparison in :mod:`normalize` is right for ordinary
German words and disastrous here. It turned "mongoose" into MongoDB,
"excels" into Excel, "swiftly" into Swift, "reacts" into React and "sparks"
into Spark -- every one of those observed, and the first of them reported
from a blank character sheet that scored well as a CV.

Technology names do not inflect, so they need no tolerance at all. Only the
long descriptive aliases do: "Reinigungsmittel" really does appear as
"Reinigungsmitteln". At eight characters a coincidence stops being
plausible."""

INFLECTIONAL_ENDINGS = frozenset({"e", "en", "er", "es", "em", "n", "s", "ns", "nen"})
"""German case and plural endings. Requiring the difference to be one of
these is what separates an inflected form from a different word that merely
starts the same way: "Datenbanken" is "Datenbank" declined, "Datenbankdesign"
is not."""


_INFLECTED_ALIASES: dict[str, str] = {}
for _alias, _id in _SINGLE_WORD_ALIASES.items():
    if len(_alias) < MIN_INFLECTED_ALIAS:
        continue
    for _ending in INFLECTIONAL_ENDINGS:
        # Same first-writer-wins order as the scan it replaces: the aliases
        # are walked in the order they were declared, so a form two aliases
        # could both produce belongs to the one that was written first.
        _INFLECTED_ALIASES.setdefault(_alias + _ending, _id)
"""Every alias that may inflect, with its endings already written out.

This was a rule applied by walking all the aliases for every unmatched word
in the text: a few hundred string comparisons per word, and half the cost of
reading an advert. The set of forms the rule can accept is small, finite and
known at import -- an alias plus one of nine endings -- so it is built once
here and looked up.

The rule runs one direction only, which the construction preserves: endings
are added to an alias, never stripped off a word. Allowing the word to be
the shorter of the two let "Schleife" (a ribbon) reach CNC through
"schleifen", "Toleranz" (an attitude) reach Messtechnik through
"toleranzen", "Workshop" reach Change Management, "transform" reach Deep
Learning and "embedding" reach RAG. Every legitimate case adds:
"Reinigungsmitteln" is "reinigungsmittel" declined, never the reverse."""


def _lookup(window: list[str], localised: dict[str, str]) -> str | None:
    """Resolve one window of folded words to a skill id.

    Exact spelling first: that is both the common case and the safe one. The
    base table is asked before the document's own language, so a name that
    exists in both is read as the one the labels are written in. Only single
    words fall back to inflection, and only long ones -- see
    :data:`MIN_INFLECTED_ALIAS` for what happens without that floor.
    """
    phrase = window[0] if len(window) == 1 else " ".join(window)
    exact = ALIAS_TO_ID.get(phrase) or localised.get(phrase)
    if exact is not None:
        return exact
    if len(window) != 1 or len(phrase) <= MIN_INFLECTED_ALIAS:
        return None
    return _INFLECTED_ALIASES.get(phrase)
