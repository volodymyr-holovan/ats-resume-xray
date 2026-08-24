"""Work out which language a document is written in.

A CV and the advert it is measured against are written in one language.
English is the exception: it turns up inside documents in every other
language, as product names, job titles and whole bullet points.

That pairing matters because the phrase vocabularies in this project overlap
across languages in ways that produce wrong answers, not just wasted work.
Spanish "diploma" sits inside German "Diplomatie"; Dutch "promotie" means a
doctorate in Dutch and a sales campaign in German. Deciding the language
once and then reading only that language's phrases plus English removes a
whole class of false positives.

Detection is a function-word count. Function words are the most frequent
words in any text, they are short, and they are almost never borrowed, which
makes them a far more reliable signal than content words for a few lines of
job advert. There is no model and no dependency: the whole method is the
table below.
"""

from .normalize import fold

FALLBACK_LANGUAGE = "en"
MIN_TOKENS = 8
"""Below this there is not enough text to count anything. A three-word
heading would be decided by a single coincidence."""

MIN_MARGIN = 2
"""How far ahead the winner must be. German and Dutch share many function
words, and a one-hit lead between them means nothing."""

HEADING_WEIGHT = 3
CHARACTER_WEIGHT = 2
"""A CV is not prose. It is a name, four headings and a list of dates, and a
terse German one can contain as few as two German function words -- which
was enough to have a real German CV read as English.

Two other signals carry more per occurrence than a function word does. A
section heading is nearly conclusive: nothing but a German CV says
"Berufserfahrung". A letter that only one of these languages uses is close
behind."""

DISTINCTIVE_CHARACTERS: dict[str, str] = {
    "de": "äöüß",
    "es": "ñ¿¡",
    "fr": "çœàèùâêîô",
    # Dutch has no letter the others lack, and Ukrainian and Russian are
    # separated by SCRIPT_MARKERS below rather than here.
}

FUNCTION_WORDS: dict[str, frozenset[str]] = {
    "de": frozenset(
        """der die das den dem des ein eine einer eines und oder aber mit von zu
        für auf im in an bei nach aus über unter durch ist sind war wird werden
        haben hat sowie nicht auch als wie wir sie ihr ihre uns unser sich""".split()
    ),
    "en": frozenset(
        """the a an and or but with from to for on in at by of is are was were
        be been have has had you your we our they their this that these those
        will would should can could as if not about into""".split()
    ),
    "es": frozenset(
        """el la los las un una unos unas y o pero con de del para por en sobre
        entre es son era ser estar tener tiene su sus nuestro nuestra que como
        no también más muy este esta estos estas""".split()
    ),
    "nl": frozenset(
        """de het een en of maar met van voor op in aan bij naar uit over onder
        door is zijn was waren worden hebben heeft ook als zoals wij jij jouw
        onze zich niet dat deze die dit meer zeer""".split()
    ),
    "fr": frozenset(
        """le la les un une des du de et ou mais avec pour sur dans par chez
        vers sous entre est sont était être avoir vous votre nous notre ils
        elles ce cette ces qui que dont plus très pas aussi""".split()
    ),
    "uk": frozenset(
        """та і й або але з із для на в у до від про над під через є були буде
        який яка які що як ми ви ваш ваша ваші наш наша не також дуже цей ця ці
        його її їх мати має""".split()
    ),
    "ru": frozenset(
        """и или но с со для на в во до от про над под через есть был были будет
        который которая которые что как мы вы ваш ваша ваши наш наша не также
        очень этот эта эти его ее их иметь имеет""".split()
    ),
}

SCRIPT_MARKERS: dict[str, frozenset[str]] = {
    "uk": frozenset("їєґі"),
    "ru": frozenset("ыъэё"),
}
"""Ukrainian and Russian share most function words, so the alphabet decides
between them: each uses letters the other does not have."""

_CYRILLIC = frozenset("абвгдежзийклмнопрстуфхцчшщьюя")


def detect_language(text: str, allowed: frozenset[str] | None = None) -> str:
    """The language ``text`` is written in, as a UI language code.

    Falls back to English rather than guessing when the text is too short or
    no language is clearly ahead: English is the safe default because its
    vocabulary is the one that is always read anyway.
    """
    words = fold(text).split()
    if len(words) < MIN_TOKENS:
        return FALLBACK_LANGUAGE

    seen = set(words)
    headings = _heading_hits(text)
    lowered = text.lower()
    scores = {
        code: (
            len(seen & vocabulary)
            + HEADING_WEIGHT * headings.get(code, 0)
            + CHARACTER_WEIGHT * bool(set(lowered) & set(DISTINCTIVE_CHARACTERS.get(code, "")))
        )
        for code, vocabulary in FUNCTION_WORDS.items()
        if allowed is None or code in allowed
    }
    if not scores:
        return FALLBACK_LANGUAGE

    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    best, best_score = ranked[0]
    runner_up = ranked[1][1] if len(ranked) > 1 else 0

    if best_score == 0 or best_score - runner_up < MIN_MARGIN:
        cyrillic = _cyrillic_choice(text, scores)
        return cyrillic or FALLBACK_LANGUAGE

    if best in SCRIPT_MARKERS:
        return _cyrillic_choice(text, scores) or best
    return best


def _heading_hits(text: str) -> dict[str, int]:
    """How many lines are a CV section heading in each language.

    Imported from the section recogniser rather than retyped, so the two
    stay in step: a heading added there immediately becomes evidence here.
    """
    # Imported late: vacancy imports this module, so a top-level import
    # here would close the loop.
    from .sections import SECTION_ALIASES_BY_LANGUAGE, normalize_heading
    from .vacancy import BLOCK_HEADINGS_BY_LANGUAGE

    lines = {normalize_heading(line) for line in text.splitlines() if line.strip()}
    if not lines:
        return {}

    hits: dict[str, int] = {}
    for code, sections in SECTION_ALIASES_BY_LANGUAGE.items():
        hits[code] = sum(1 for aliases in sections.values() for alias in aliases if alias in lines)
    # An advert has no CV section headings but does have its own -- and
    # "Requisitos" identifies Spanish as surely as "Berufserfahrung"
    # identifies German.
    for code, blocks in BLOCK_HEADINGS_BY_LANGUAGE.items():
        hits[code] = hits.get(code, 0) + sum(
            1 for headings in blocks.values() for heading in headings
            if any(heading in line for line in lines)
        )
    return hits


def _cyrillic_choice(text: str, scores: dict[str, int]) -> str | None:
    """Ukrainian or Russian, decided by the letters only one of them uses.

    Reached both when Cyrillic clearly won and when nothing did: a short
    Cyrillic advert loses on function-word count but is still obviously not
    English.
    """
    lowered = text.lower()
    if not any(ch in _CYRILLIC for ch in lowered):
        return None
    hits = {
        code: sum(ch in markers for ch in lowered)
        for code, markers in SCRIPT_MARKERS.items()
        if code in scores
    }
    if not hits or not any(hits.values()):
        return max(
            (code for code in SCRIPT_MARKERS if code in scores),
            key=lambda code: scores.get(code, 0),
            default=None,
        )
    return max(hits, key=lambda code: hits[code])


def vocabulary_languages(language: str) -> tuple[str, ...]:
    """Which language's phrases to read for a document in ``language``.

    Always the document's own language and English, because English phrases
    appear inside documents written in every other language and excluding
    them would lose real requirements.
    """
    if language == FALLBACK_LANGUAGE:
        return (FALLBACK_LANGUAGE,)
    return (language, FALLBACK_LANGUAGE)


def merge_for(mapping: dict, language: str) -> tuple:
    """Flatten a per-language mapping down to the languages worth reading."""
    merged: list = []
    for code in vocabulary_languages(language):
        merged.extend(mapping.get(code, ()))
    return tuple(merged)
