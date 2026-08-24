"""Text normalisation shared by vacancy parsing and CV matching.

Matching a job advert against a CV is mostly a spelling problem. The advert
says "Qualitätssicherung", the CV says "Qualitaetssicherung"; the advert
says "Erfahrungen", the CV says "Erfahrung"; one writes "Node.js", the other
"NodeJS". None of that is a real difference, and treating it as one produces
a match report full of false gaps, which is worse than no report at all.

The rules here are deliberately small and explicit rather than a
morphological analyser. Every one of them can be read, tested, and argued
with, which matters because a wrong normalisation silently changes the
score and nobody would know why.
"""

import re
import unicodedata

UMLAUT_EXPANSIONS = {
    "ä": "ae",
    "ö": "oe",
    "ü": "ue",
    "Ä": "ae",
    "Ö": "oe",
    "Ü": "ue",
    "ß": "ss",
}
"""German umlauts spelled out. Applied *before* diacritic stripping so that
"Qualität" and the ASCII "Qualitaet" land on the same string. Doing it the
other way round ("ä" -> "a") would leave them apart, which is the more
common spelling difference in job adverts written on foreign keyboards."""

MIN_PREFIX_STEM = 5
"""Shortest shared beginning that may count as the same stem. Below this,
near-identical short tokens mean genuinely different things -- "SQL" and
"SQLite" share three letters and are not the same skill."""

MAX_PREFIX_GAP = 3
"""How much may hang off the end of *each* word beyond the shared stem.

Comparing the tails on both sides rather than requiring one word to be a
prefix of the other is what catches German adjective endings, where the
ending replaces a letter instead of adding one: "maschinelles" and
"maschinellem" share eleven letters and differ by one on each side."""

# Unicode-aware on purpose: an ASCII-only class would erase Cyrillic and
# Greek entirely, and a heading that folds to the empty string then matches
# every line of every document.
_NON_WORD = re.compile(r"[^\w+#.]+|_+", re.UNICODE)
_MULTI_SPACE = re.compile(r"\s+")


def fold(text: str) -> str:
    """Lower-case, expand umlauts, drop remaining diacritics.

    Punctuation is kept where it carries meaning in a technology name --
    ``+`` for C++, ``#`` for C#, ``.`` for .NET and Node.js -- and turned
    into a space everywhere else.
    """
    for umlaut, expansion in UMLAUT_EXPANSIONS.items():
        text = text.replace(umlaut, expansion)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower()
    text = _NON_WORD.sub(" ", text)
    text = _MULTI_SPACE.sub(" ", text).strip()
    # A sentence-ending dot would otherwise fuse into the word before it and
    # stop "Docker." from matching "Docker". Dots inside a word are left
    # alone, because that is where they carry meaning: node.js, asp.net.
    return " ".join(word.rstrip(".") or word for word in text.split())


def tokens(text: str) -> list[str]:
    folded = fold(text)
    return folded.split() if folded else []


def same_word(left: str, right: str) -> bool:
    """Whether two already-folded words are the same word inflected.

    A shared-stem comparison rather than a stemmer: German inflection sits
    at the end of the word, so a long common beginning with a short tail on
    either side is the signal, and the two guards above stop it from
    reaching far enough to join unrelated words.
    """
    if left == right:
        return True
    stem = _shared_prefix_length(left, right)
    if stem < MIN_PREFIX_STEM:
        return False
    return len(left) - stem <= MAX_PREFIX_GAP and len(right) - stem <= MAX_PREFIX_GAP


def _shared_prefix_length(left: str, right: str) -> int:
    length = 0
    for a, b in zip(left, right):
        if a != b:
            break
        length += 1
    return length


def contains_phrase(haystack_tokens: list[str], phrase: str) -> bool:
    """Whether a folded multi-word phrase appears in a token list.

    Words are compared with :func:`same_word`, so "Maschinelles Lernen"
    in the advert matches "maschinellem Lernen" in the CV.
    """
    needle = phrase.split()
    if not needle or len(needle) > len(haystack_tokens):
        return False
    for start in range(len(haystack_tokens) - len(needle) + 1):
        window = haystack_tokens[start : start + len(needle)]
        if all(same_word(a, b) for a, b in zip(window, needle)):
            return True
    return False
