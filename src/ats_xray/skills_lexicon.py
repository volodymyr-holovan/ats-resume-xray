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
from .skills_data import ALL_SKILLS


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

AMBIGUOUS_ALIASES = frozenset({"go", "r", "c", "ad", "ai", "ki", "qa", "hr", "au", "hu", "bar", "din", "iso", "sap fi", "sap co"})
"""Spellings that are never treated as a skill mention even though they are
the real name of one.

"Go live", "R&D", "a.i.", "ad hoc", "HR" inside a German sentence, "Bar" as
a place rather than the craft: each is an ordinary word somewhere, and a
requirements list that gained a programming language from a launch date
would be wrong in a way the reader cannot easily spot. Every skill here
stays reachable through a longer, unambiguous alias.
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

MAX_ALIAS_WORDS = max(len(alias.split()) for alias in ALIAS_TO_ID)

_SINGLE_WORD_ALIASES: dict[str, str] = {
    alias: skill_id for alias, skill_id in ALIAS_TO_ID.items() if " " not in alias
}


def label_for(skill_id: str) -> str:
    skill = SKILLS_BY_ID.get(skill_id)
    return skill.label if skill else skill_id


def category_for(skill_id: str) -> str:
    skill = SKILLS_BY_ID.get(skill_id)
    return skill.category if skill else "other"


def find_skills(text: str) -> list[str]:
    """Skill ids mentioned in ``text``, in order of first appearance."""
    return find_skills_and_covered(text)[0]


def find_skills_and_covered(text: str) -> tuple[list[str], set[str]]:
    """Skill ids plus the folded words those matches used up.

    The second half exists for the generic term extractor: a word already
    explained by a lexicon hit must not come back as a separate keyword, or
    "Microsoft SQL Server" would be reported once as a skill and three more
    times as loose nouns.
    """
    words = fold(text).split() if text else []
    consumed = [False] * len(words)
    found: list[str] = []

    for size in range(min(MAX_ALIAS_WORDS, len(words)), 0, -1):
        for start in range(len(words) - size + 1):
            if any(consumed[start : start + size]):
                continue
            skill_id = _lookup(words[start : start + size])
            if skill_id is None:
                continue
            for index in range(start, start + size):
                consumed[index] = True
            if skill_id not in found:
                found.append(skill_id)

    covered = {word for word, used in zip(words, consumed) if used}
    return found, covered


def _lookup(window: list[str]) -> str | None:
    """Resolve one window of folded words to a skill id.

    Tries the exact spelling first, because that is both the common case and
    the safe one. Only single words fall back to inflection-tolerant
    comparison: allowing it on every phrase would make long aliases match
    far too loosely.
    """
    from .normalize import same_word

    phrase = " ".join(window)
    exact = ALIAS_TO_ID.get(phrase)
    if exact is not None:
        return exact
    if len(window) != 1:
        return None
    for alias, skill_id in _SINGLE_WORD_ALIASES.items():
        if same_word(alias, phrase):
            return skill_id
    return None
