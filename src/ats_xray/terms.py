"""Pull requirement keywords out of an advert the lexicon does not know.

A curated lexicon is accurate and finite. It cannot cover every trade, every
certificate and every piece of equipment a job might name, and an advert for
a profession nobody thought to add would otherwise produce an empty
requirements list -- which is worse than a rough one, because the reader has
nothing to correct.

What this module has to get right is not finding candidates. Candidates are
everywhere. It is rejecting them, and the three rules below do most of that
work structurally rather than by listing words.

*Where the line sits decides what may be harvested.* An advert names its
blocks, and they mean different things. The profile block states what the
candidate must bring; the tasks block describes the work and names the
things the work is done to. Mining nouns out of the tasks block is where
almost all of the noise came from: "Buchung von Warenbewegungen", "Entladen
von Sendungen", "Zusammenarbeit mit Angehörigen" are duties, and none of
them is anything a person can claim to have. So the tasks block is read
through requirement phrases only, and its loose nouns are left alone. What
that gives up is a real system name occasionally mentioned only under the
duties; what it removes is roughly six noise terms for every real one.

*Only German capitalises its common nouns.* Every requirement worth
extracting from a German advert is a noun and almost nothing else in the
sentence is capitalised, which is a better part-of-speech tagger than
anything that would fit in this project's dependencies. In the other six
languages a capital letter marks the start of a bullet and nothing else, so
the same rule harvested verbs: "Take part in the on-call rotation" gave
"Take", "Montaje y desmontaje de mesas" gave "Montaje", "Приготовление блюд"
gave "Приготовление". The capitalisation signal is now used where it means
something and switched off where it does not.

*Every language announces requirements with the same few phrases.*
"Kenntnisse in", "Erfahrung mit", "experience with", "conocimiento de",
"досвід роботи з". What follows one of those is a requirement by
construction, in any of the seven languages the app speaks. Those phrases
carry the whole load in the six languages that have no capitalisation
signal, so they have to be generous, and what they over-capture is cut back
by the per-language trimming below rather than by refusing to match.

Everything that survives is still a guess, and the interface shows it in an
editable list before anything is scored.
"""

import re
from dataclasses import dataclass

from .credentials import LANGUAGE_NAMES_BY_LANGUAGE
from .langid import FUNCTION_WORDS, merge_for
from .normalize import fold
from .skills_lexicon import find_skills_and_covered

MIN_TERM_LENGTH = 4
MAX_PHRASE_WORDS = 3
MAX_TERMS_PER_AD = 20
"""An advert that yields more than this is producing noise, not
requirements, and a list too long to read is a list nobody will correct."""

UPPERCASE_LINE_RATIO = 0.8
"""Above this share of capitals a line is a shouted heading, not a sentence.
Every word in it looks like a German noun, so the capitalisation signal
carries no information and is skipped for that line."""

NOUN_CAPITALISING_LANGUAGES = frozenset({"de"})
"""Languages where a capital letter inside a sentence marks a noun.

German, and only German, of the seven. Dutch capitalises no common nouns
despite the family resemblance, and the other five capitalise a bullet's
first word exactly as English does."""

WEIGHT_INTRODUCED = 3
"""A requirement phrase names it outright: "Kenntnisse in X"."""
WEIGHT_NOUN = 2
"""A capitalised noun in the block that states requirements."""
WEIGHT_TASK = 1
"""A requirement phrase inside the duties. Real, and the weakest evidence
there is: the sentence is about the work, not about the candidate."""

BLOCK_SOURCES: dict[str, tuple[str, ...]] = {
    "profile": ("introduced", "noun"),
    "intro": ("introduced", "noun"),
    "tasks": ("introduced",),
}
"""What may be harvested where. An unlisted block gets the cautious reading:
a block this parser could not name is not a licence to mine it."""

DEFAULT_BLOCK = "profile"


@dataclass(frozen=True)
class Candidate:
    """One guessed keyword and how it was found.

    ``weight`` exists so the cap can drop the weakest rather than whatever
    the loop reached last. Two adverts out of five produced more candidates
    than the cap allows, and the ones being discarded were arriving in line
    order.
    """

    text: str
    weight: int


_STRUCTURE_WORDS = (
    # Function words that get capitalised at the start of a bullet.
    "der", "die", "das", "dem", "den", "des", "ein", "eine", "einen", "einem", "einer",
    "und", "oder", "mit", "für", "von", "vom", "bei", "als", "auch", "sowie", "nach",
    "aus", "auf", "unter", "über", "durch", "zur", "zum", "sind", "ist", "wird",
    "werden", "haben", "hat", "kann", "können", "sollte", "sollten", "muss", "müssen",
    "sie", "ihr", "ihre", "ihren", "ihnen", "wir", "uns", "unser", "unsere", "dich",
    "dein", "deine", "deinen", "you", "your", "our", "the", "and", "with", "for",
    "from", "are", "will", "should", "must", "have", "has", "this", "that",
)

_MODIFIERS = (
    # Adjectives and participles that open a German requirement bullet. They
    # are capitalised there purely by sentence position.
    "abgeschlossene", "abgeschlossenes", "abgeschlossener", "abgeschlossenem",
    "gute", "guter", "gutes", "guten", "sehr", "mindestens", "wenigstens",
    "sicherer", "sicheres", "sichere", "sicherem", "gültige", "gültiger", "gültiges",
    "staatlich", "anerkannte", "anerkannter", "erweitertes", "erweiterte",
    "fundierte", "fundiertes", "fundierter", "ausgeprägte", "ausgeprägtes",
    "hohe", "hohes", "hoher", "hohem", "selbstständige", "selbständige",
    "strukturierte", "erste", "ersten", "mehrjährige", "langjährige", "einschlägige",
    "idealerweise", "wünschenswert", "wünschenswerte", "nachweisbare", "nachgewiesene",
    "praktische", "theoretische", "umfassende", "grundlegende", "solide", "solides",
    "optimalerweise", "vorzugsweise", "zwingend", "erforderlich", "erforderliche",
    "notwendig", "notwendige", "alternativ", "darüber", "zudem", "außerdem",
    "weiterhin", "entsprechende", "entsprechendes", "versierte", "routinierte",
    "souveräne", "engagierte", "motivierte", "freundliche", "gepflegtes", "gepflegte",
    "erfolgreich", "erfolgreiche", "vorhandene", "verhandlungssichere", "fließende",
    "excellent", "strong", "good", "proven", "solid", "demonstrated", "fluent",
    "native", "relevant", "prior", "previous", "extensive", "deep", "basic",
    "advanced", "working", "outstanding", "ideally", "preferably", "several",
    "willingness", "passion", "familiarity", "proficiency", "hands-on",
    "completed", "afgeronde", "vloeiend", "diplome", "estudios",
    # "... is required", "... est exigee", "... es imprescindible": the
    # sentence saying a requirement is one. German has these above; these are
    # the languages that put them after the noun rather than before it.
    "required", "preferred", "essential", "desirable", "mandatory", "welcome",
    "exige", "exigee", "exigees", "exiges", "requis", "requise", "requises",
    "souhaite", "souhaitee", "souhaitees", "obligatoire", "indispensable",
    "imprescindible", "imprescindibles", "necesario", "necesaria", "requerido",
    "requerida", "valorable", "valorables", "deseable", "deseables",
    "vereist", "gewenst", "noodzakelijk",
    "technische", "technisches", "technischer", "direkter", "direkte",
    "moderne", "modernes", "hochwertiges", "attraktive", "gründliche",
    "abwechslungsreiches", "innovativem", "wichtige", "verschiedene",
    # The people a job serves are not a skill.
    "bewohner", "patienten", "patient", "gäste", "gast", "klienten", "nutzer",
    "anwender", "besucher", "bewerber", "schüler", "teilnehmer", "personen",
    "menschen", "bürger", "mandanten", "gemeinde", "kinder", "jugendliche",
    "eltern", "angehörigen", "ärzten", "therapeuten", "kollegen", "kolleginnen",
    # What is left over when a compound's first half was a lexicon hit:
    # "HACCP-Vorgaben" must not come back as a requirement called "Vorgaben".
    "vorgabe", "vorgaben", "regelungen", "bestimmungen", "grundsätze",
    "kriterien", "aspekte", "inhalte", "punkte", "verfahren", "methoden",
    "methode", "methoden", "metodo", "metodos", "method", "methods",
    "maßnahmen", "abläufe", "vorschriften", "unterlagen", "dokumente",
)

_HEAD_NOUNS = (
    # Framing words that are still the head of the phrase they end. Trimming
    # them off the front of "Planung der Einsaetze" is right; trimming them
    # off the end of "lesson planning" leaves "lesson", which is not what the
    # advert asked for. They stay in STOPWORDS, so alone they are still
    # dropped -- this only stops the trailing trim from eating them.
    "planning", "production", "rotation",
)

_FRAMING_WORDS = _HEAD_NOUNS + (
    # Words that frame a requirement without being one.
    "kenntnis", "kenntnisse", "kenntnissen", "erfahrung", "erfahrungen", "umgang",
    "bereich", "bereichen", "jahre", "jahren", "vorteil", "profil", "aufgabe",
    "aufgaben", "anforderung", "anforderungen", "voraussetzung", "voraussetzungen",
    "ausbildung", "studium", "berufserfahrung", "abschluss", "qualifikation",
    "bereitschaft", "fähigkeit", "fähigkeiten", "freude", "spaß", "interesse",
    "motivation", "einsatz", "einsatzbereitschaft", "möglichkeit", "rahmen",
    "grundlage", "grundlagen", "verständnis", "denken", "arbeitsweise", "umfeld",
    "klasse", "modul", "module", "richtlinien", "richtlinie", "einhaltung",
    "durchführung", "sinne", "vorteilhaft", "nachweis", "niveau", "wort", "schrift",
    "experience", "knowledge", "skills", "skill", "ability", "years", "requirements",
    "qualifications", "understanding", "background", "plus", "advantage", "level",
    # Handled by the typed extractors, so never a loose keyword.
    "deutsch", "englisch", "deutschkenntnisse", "englischkenntnisse", "sprache",
    "sprachkenntnisse", "german", "english", "führerschein", "fahrerlaubnis",
    "rijbewijs", "permis", "carné", "carne", "bachelor", "master", "diplom",
    "promotion", "degree", "diploma",
    # Company and posting boilerplate.
    "paragraf", "paragraph", "absatz", "abs", "satz",
    "unternehmen", "firma", "arbeitgeber", "stelle", "position", "team", "teams",
    "mitarbeiter", "mitarbeiterinnen", "kunden", "kunde", "bewerbung",
    "gehalt", "woche", "wochen", "stunden", "monat", "monate", "euro", "urlaub",
    "arbeit", "arbeiten", "tätigkeit", "tätigkeiten", "alltag", "standort",
    "company", "role", "job", "work", "salary", "benefits", "week", "month",
    # Language names: levels are read by the typed extractor, so the bare
    # name is never a loose keyword.
    "russisch", "russian", "ukrainisch", "ukrainian", "französisch", "french",
    "spanisch", "spanish", "niederländisch", "dutch", "italienisch", "italian",
    "polnisch", "polish", "türkisch", "turkish", "chinesisch", "chinese",
    # Frequent leftovers from German requirement bullets.
    "deutsche", "deutscher", "deutschen", "teilnahme", "liebe", "detail",
    "umfang", "menge", "art", "weise", "seite", "punkt", "thema", "themen",
    "ihrem", "ihrer", "diesem", "dieser", "beispiel", "sinn", "hand",
    "system", "systeme", "systemen", "systems", "software", "programme",
    "anwendung", "anwendungen", "tools", "werkzeuge", "produkte", "projekt",
    "projekte", "projekten", "prozesse", "prozessen", "abteilung", "branche",
    "konzept", "konzepte", "ansatz", "portfolio",
    # Spanish
    "conocimiento", "conocimientos", "experiencia", "estudios", "titulacion",
    "perfil", "requisitos", "funciones", "ofrecemos", "anos", "años", "capacidad",
    "dominio", "nivel", "buen", "buena", "alto", "alta", "imprescindible",
    "valorable", "deseable", "empresa", "puesto", "equipo", "menos", "apoyo",
    # Dutch
    "kennis", "ervaring", "opleiding", "profiel", "vereisten", "taken",
    "jaar", "jaren", "goede", "sterke", "afgeronde", "vloeiend", "pre",
    "vaardigheden", "bedrijf", "functie", "werkzaamheden", "niveau",
    # French
    "connaissance", "connaissances", "experience", "diplome", "missions",
    "exigences", "bonne", "bonnes", "maitrise", "souhaite", "atout",
    "entreprise", "poste", "equipe", "competences", "ans", "minimum", "courant",
    # Ukrainian
    "знання", "досвід", "освіта", "вища", "вищу", "профіль", "вимоги",
    "обов", "язки", "роки", "років", "рівень", "володіння", "бажано",
    "обовязково", "компанія", "посада", "команда", "навички", "участь",
    # Russian
    "знание", "опыт", "образование", "высшее", "профиль", "требования",
    "обязанности", "годы", "лет", "уровень", "владение", "желательно",
    "обязательно", "компания", "должность", "команда", "навыки", "нормы",
    # Slavic bullets open with these the way German ones open with
    # "Abgeschlossene": they quantify the requirement, they are not it.
    "щонайменше", "не менше", "принаймні", "профільна", "профільне",
    "закінчена", "закінчене", "чинна", "чинне", "впевнене", "готовність",
    "бажання", "уміння", "вміння", "не менее", "профильное", "профильная",
    "законченное", "действующая", "уверенное", "готовность", "желание",
    "умение", "высшее", "среднее", "начальное",
    # Slavic predicates close a requirement line rather than open it, so
    # they arrive on the tail of a captured phrase: "Лицензия охранника
    # обязательна" is one requirement and one verdict on it.
    "обов'язковий", "обов'язкова", "обов'язкове", "обов'язковим", "обов'язково",
    "обязателен", "обязательна", "обязательно", "обязательное",
    "бажаний", "бажана", "бажане", "желателен", "желательна", "желательно",
    "вітається", "приветствуется", "необхідний", "необхідна", "необходим",
    "необходима", "необходимо",
)

_NUMERAL_STEMS: dict[str, tuple[str, ...]] = {
    "de": ("ein", "zwei", "drei", "vier", "fünf", "sechs", "sieben", "acht", "neun", "zehn"),
    "en": ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"),
    "es": ("uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez"),
    "nl": ("een", "twee", "drie", "vier", "vijf", "zes", "zeven", "acht", "negen", "tien"),
    "fr": ("un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf", "dix"),
    "uk": ("одн", "дв", "тр", "чотир", "п'ят", "пят", "шест", "сем", "сім", "вісьм", "десят"),
    "ru": ("одн", "дв", "тр", "четыр", "пят", "шест", "сем", "восьм", "девят", "десят"),
}
"""Spelled numbers, as stems because they decline.

"Досвід роботи з React від трьох років" put "трьох" forward as a
requirement once the preposition was trimmed off it. A number is never the
thing being asked for -- the typed years extractor reads it properly -- so a
candidate that is only a number is dropped whatever its spelling."""

_SLAVIC_ADJECTIVE_ENDINGS = (
    "ого", "ому", "ими", "ыми", "ий", "ый", "ая", "яя", "ое", "ее", "ые", "ие",
    "ой", "ей", "ою", "ою", "их", "ых", "ым", "им", "ій", "ої", "ою", "і",
)
"""Endings that mark a Russian or Ukrainian adjective.

Applied only to a candidate that is a single word. "Медицинская книжка
обязательна" left "Медицинская" standing alone once the noun was trimmed,
and an adjective with no noun names nothing. Inside a phrase the adjective
is doing its job -- "санитарных норм" is a real requirement -- so the rule
never looks at a word with a neighbour."""

_SLAVIC_INFINITIVE_ENDINGS = ("ти", "ть", "тись", "ться")
"""Ukrainian and Russian mark the infinitive at the end of the word.

"Умение работать с пароконвектоматом" is a requirement whose subject is the
last word; the introducer catches "умение" and the verb is left leading the
phrase. Dropping a leading infinitive is safe in these two languages and
wrong in Dutch and German, where the infinitive is also the ordinary way to
name an activity -- "lassen" and "Schweißen" both mean welding and both are
real requirements."""

_EXTRA_EDGE_WORDS: dict[str, tuple[str, ...]] = {
    "de": ("im", "in", "am", "an", "zu", "zur", "zum", "des", "beim"),
    "en": ("of", "in", "on", "at", "as", "least", "using"),
    "es": ("al", "del", "de", "en", "con", "por", "para", "sobre"),
    "nl": ("van", "met", "in", "op", "aan", "bij", "is", "een"),
    "fr": ("de", "des", "du", "en", "dans", "avec", "sur", "la", "le", "les"),
    "uk": ("з", "із", "у", "в", "до", "від", "на", "та", "і", "й", "або", "по"),
    "ru": ("с", "со", "в", "во", "до", "от", "на", "и", "или", "по", "для"),
}
"""Words allowed to sit at the edge of a captured phrase and never inside a
requirement.

The function-word tables in :mod:`langid` are the bulk of this and are
reused rather than retyped, but they are built to identify a language, not
to trim a phrase, so a few prepositions each language leans on are missing
from them."""

_LANGUAGE_NAMES = tuple(
    name
    for per_language in LANGUAGE_NAMES_BY_LANGUAGE.values()
    for names in per_language.values()
    for name in names
)
"""Taken from the language extractor rather than retyped, so a language
added there can never start leaking out of here as a loose keyword."""

_LANGUAGE_PREFIXES = tuple(sorted({fold(name) for name in _LANGUAGE_NAMES if fold(name)}))
"""The same names matched as prefixes, because they are declined:
"Німецька", "німецькою" and "Deutschkenntnisse" all grow out of a stem that
the exact-match stoplist would miss."""

STOPWORDS = frozenset(
    fold(word)
    for word in (_STRUCTURE_WORDS + _MODIFIERS + _FRAMING_WORDS + _LANGUAGE_NAMES)
)

INTRODUCERS_BY_LANGUAGE: dict[str, tuple[str, ...]] = {
    "de": (
        r"kenntnisse?\s+(?:in|im|über|von|mit)",
        r"erfahrung(?:en)?\s+(?:mit|in|im|als|bei)",
        r"(?:sicherer\s+)?umgang\s+mit",
        r"routine\s+(?:in|im)",
        r"vertraut\s+mit",
        r"ausbildung\s+(?:als|zum|zur|im|in)",
        r"studium\s+(?:der|des|in|im)",
    ),
    "en": (
        r"experience\s+(?:with|in|of|as)",
        r"knowledge\s+of",
        r"proficiency\s+(?:in|with)",
        r"familiarity\s+with",
        r"skills?\s+in",
        r"degree\s+in",
        r"background\s+in",
    ),
    # Spanish and French write no capital on their nouns, so these patterns
    # carry the whole load and have to be generous. Accents are optional
    # because half of all adverts are typed without them.
    "es": (
        r"experiencia\s+(?:en|con|de|del)",
        r"conocimientos?\s+(?:de|en|del|sobre)",
        r"dominio\s+(?:de|del)",
        r"manejo\s+(?:de|del)",
        r"formaci[óo]n\s+(?:en|de|profesional\s+en)",
        r"titulaci[óo]n\s+(?:en|de)",
        r"nivel\s+(?:de|alto\s+de)",
        r"carn[ée]\s+de",
    ),
    "nl": (
        r"ervaring\s+(?:met|in)",
        r"kennis\s+van",
        r"opleiding\s+(?:in|tot)",
        r"vaardigheid\s+(?:in|met)",
    ),
    "fr": (
        r"exp[ée]rience\s+(?:en|avec|dans|de|des|du|d')",
        r"connaissances?\s+(?:de|des|du|en|d')",
        r"ma[iî]trise\s+(?:de|des|du|d')",
        r"comp[ée]tences?\s+(?:en|de|des)",
        r"formation\s+(?:en|de|dans)",
        r"dipl[oô]me\s+(?:en|de|d')",
        r"titulaire\s+(?:de|d'|du)",
        r"pratique\s+(?:de|des|du)",
    ),
    # Ukrainian and Russian put the requirement in the genitive with no
    # preposition at all -- "досвід охорони об'єктів", "опыт охраны
    # объектов" -- so a pattern that insists on one finds nothing in half
    # the adverts. These two have no capitalisation signal to fall back on,
    # which makes the introducer the only route in and a missed match a
    # requirements list with nothing in it.
    "uk": (
        r"досвід(?:\s+роботи)?(?:\s+(?:з|у|в|із|на|по))?",
        r"знання(?:\s+(?:з|у|в|про))?",
        r"володіння",
        r"вміння",
        r"навички(?:\s+(?:з|у|в))?",
        r"сертифікат\s+(?:з|про)",
        r"ліцензія(?:\s+на)?",
        r"дозвіл\s+на",
    ),
    "ru": (
        r"опыт(?:\s+работы)?(?:\s+(?:с|в|со|на|по))?",
        r"знание(?:\s+(?:в|по|о))?",
        r"владение",
        r"умение",
        r"навыки(?:\s+(?:в|по))?",
        r"сертификат\s+(?:о|по)",
        r"лицензия(?:\s+на)?",
        r"разрешение\s+на",
    ),
}

ARTICLES_BY_LANGUAGE: dict[str, tuple[str, ...]] = {
    "de": ("der", "die", "das", "dem", "den", "einer", "einem", "eines"),
    "en": ("the", "a", "an"),
    "es": ("el", "la", "los", "las", "un", "una"),
    "nl": ("het", "de", "een"),
    "fr": ("le", "la", "les", "un", "une"),
    "uk": (),
    "ru": (),
}
"""Articles are skipped between the introducer and the keyword. Kept per
language and matched as whole words: an unanchored alternation let the
Spanish "el" bite the "El" off German "Elektronik", and the requirement came
back as "ektronik"."""


def _introduced_pattern(language: str) -> re.Pattern:
    """Compiled once per language and cached: the pattern is rebuilt on every
    advert line otherwise, and an advert has a lot of lines."""
    cached = _PATTERN_CACHE.get(language)
    if cached is None:
        introducers = merge_for(INTRODUCERS_BY_LANGUAGE, language)
        articles = merge_for(ARTICLES_BY_LANGUAGE, language)
        # The article must be a whole word followed by space, so it can only
        # ever consume an article.
        skip = r"(?:(?:" + "|".join(articles) + r")\s+)?" if articles else ""
        cached = re.compile(
            r"(?:" + "|".join(introducers) + r")\s+" + skip
            + r"([\w\-']+(?:\s+[\w\-']+){0,%d})" % (MAX_PHRASE_WORDS - 1),
            re.IGNORECASE | re.UNICODE,
        )
        _PATTERN_CACHE[language] = cached
    return cached


def _head_nouns() -> frozenset[str]:
    """Folded words the trailing trim leaves alone. See ``_HEAD_NOUNS``."""
    global _HEAD_CACHE
    if _HEAD_CACHE is None:
        _HEAD_CACHE = frozenset(fold(word) for word in _HEAD_NOUNS)
    return _HEAD_CACHE


def _edge_words(language: str) -> frozenset[str]:
    """Folded words that may be trimmed off either end of a phrase.

    Cached per language: this is three set unions and a comprehension over a
    few hundred words, and it was being rebuilt for every candidate on every
    line of every advert."""
    cached = _EDGE_CACHE.get(language)
    if cached is None:
        words: set[str] = set(STOPWORDS)
        for code in (language, "en"):
            words |= {fold(word) for word in FUNCTION_WORDS.get(code, ())}
            words |= {fold(word) for word in _EXTRA_EDGE_WORDS.get(code, ())}
        cached = frozenset(word for word in words if word)
        _EDGE_CACHE[language] = cached
    return cached


_PATTERN_CACHE: dict[str, re.Pattern] = {}
_EDGE_CACHE: dict[str, frozenset[str]] = {}
_HEAD_CACHE: frozenset[str] | None = None
_NUMERAL_CACHE: dict[str, tuple[str, ...]] = {}

_CAPITALISED = re.compile(r"(\w*[^\W\d_]\w*)", re.UNICODE)
_SPLIT_ON = re.compile(r"\s+(?:und|oder|sowie|and|or|y|en|et|та|и|или)\s+|[,;:()/]", re.IGNORECASE)
_HAS_DIGIT = re.compile(r"\d")


def extract_candidates(
    line: str,
    language: str = "en",
    block: str = DEFAULT_BLOCK,
    covered: set[str] | None = None,
) -> list[Candidate]:
    """Guessed requirement keywords in one advert line, with their evidence.

    ``covered`` is the set of folded words a lexicon match already used up,
    which the caller has usually computed already; recomputing it here meant
    scanning every line against the gazetteer twice.
    """
    if covered is None:
        covered = find_skills_and_covered(line, language)[1]
    sources = BLOCK_SOURCES.get(block, ("introduced",))
    found: list[Candidate] = []

    if "introduced" in sources:
        weight = WEIGHT_INTRODUCED if block != "tasks" else WEIGHT_TASK
        for match in _introduced_pattern(language).finditer(line):
            for part in _SPLIT_ON.split(match.group(1)):
                _collect(part, covered, found, language, weight)

    if "noun" in sources and language in NOUN_CAPITALISING_LANGUAGES and not _is_shouted(line):
        for word in _capitalised_nouns(line):
            _collect(word, covered, found, language, WEIGHT_NOUN)

    return _drop_words_already_inside_a_phrase(found)


def _drop_words_already_inside_a_phrase(found: list[Candidate]) -> list[Candidate]:
    """Remove a one-word guess that a longer guess from the same line holds.

    Both routes read the same bullet, so "Ausbildung als Mediengestalter
    Digital und Print" arrived as the phrase "Mediengestalter Digital" and
    again as the bare nouns inside it. The phrase is the better answer and
    the words under it are the same requirement said twice.
    """
    phrases = [set(fold(c.text).split()) for c in found if " " in c.text]
    if not phrases:
        return found
    return [
        candidate
        for candidate in found
        if " " in candidate.text
        or not any(fold(candidate.text) in phrase for phrase in phrases)
    ]


def extract_terms(
    line: str,
    language: str = "en",
    block: str = DEFAULT_BLOCK,
    covered: set[str] | None = None,
) -> list[str]:
    """The same guesses as plain strings, best evidence first."""
    candidates = extract_candidates(line, language, block, covered)
    return [candidate.text for candidate in sorted(candidates, key=lambda c: -c.weight)]


def _capitalised_nouns(line: str) -> list[str]:
    """Capitalised words in a German line, minus the ones that are not nouns.

    Two positions are excluded. A word directly followed by a hyphen and a
    space is the head of an elided compound -- "Grund- und
    Behandlungspflege" -- and on its own it names nothing; the full second
    half is captured anyway. And the first word of a bullet followed by
    another capitalised word is an adjective or participle standing in front
    of its noun: "Fachgerechte Grundpflege", "Abgeschlossene Ausbildung".
    German writes those lowercase everywhere except here, so position is the
    only thing that gives them away, and the noun behind them is the one
    being asked for.
    """
    words = _CAPITALISED.findall(line)
    kept: list[str] = []
    for index, word in enumerate(words):
        if not word[:1].isupper():
            continue
        if _is_elided_head(line, word):
            continue
        if index == 0 and len(words) > 1 and words[1][:1].isupper():
            continue
        kept.append(word)
    return kept


def _is_elided_head(line: str, word: str) -> bool:
    """Whether the word appears as the first half of an elided compound.

    "Fort- und Weiterbildungen" is Fortbildungen and Weiterbildungen; the
    hyphen stands in for a head this parser cannot reconstruct, since
    finding it means segmenting the second compound. Reporting "Fort" is
    worse than reporting nothing, so the half-word is dropped and the whole
    one beside it is kept.
    """
    return f"{word}- " in line or f"{word}-\n" in line or line.endswith(f"{word}-")


def _is_shouted(line: str) -> bool:
    letters = [ch for ch in line if ch.isalpha()]
    if len(letters) < 3:
        return False
    return sum(ch.isupper() for ch in letters) / len(letters) >= UPPERCASE_LINE_RATIO


def _is_elided_tail(word: str) -> bool:
    """Whether a word is the tail of an elided German compound.

    "Fehlersuche und -behebung" means Fehlersuche and Fehlerbehebung; the
    hyphen stands in for the head. Reporting "behebung" on its own names
    nothing, and the reader cannot trace it back to the advert.
    """
    return word.lstrip(" ").startswith(("-", "–", "—"))


ELIDING_LANGUAGES = frozenset({"fr"})
"""Languages that glue a one-letter article to the next word with an
apostrophe.

French "Maitrise de Sage et d'Excel" hands back "d'Excel", which is Excel
with two characters in front of it: not the same string as the lexicon's
entry, so the requirement was reported twice, once correctly and once as a
guess nobody typed. Only French of the seven does this. Ukrainian and
Russian use the apostrophe inside words -- "п'ять", "об'єкт" -- so the same
rule there would cut real words in half."""

_ELISION = re.compile(r"^\w{1,2}['’](?=\w)", re.UNICODE)


def _drop_elision(word: str) -> str:
    return _ELISION.sub("", word)


def _folded_numerals(language: str) -> tuple[str, ...]:
    """Cached: the stems are constants and were being folded again for every
    word at both ends of every candidate."""
    cached = _NUMERAL_CACHE.get(language)
    if cached is None:
        stems = _NUMERAL_STEMS.get(language, ()) + _NUMERAL_STEMS["en"]
        cached = tuple(sorted({folded for folded in map(fold, stems) if folded}))
        _NUMERAL_CACHE[language] = cached
    return cached


def _is_numeral(folded_word: str, language: str) -> bool:
    if _HAS_DIGIT.search(folded_word):
        return True
    return folded_word.startswith(_folded_numerals(language))


def _trim(candidate: str, language: str) -> str:
    """Drop framing words, prepositions and numbers from both ends.

    "Pflegedokumentation sind zwingend" is the phrase pattern doing its job
    and then running past the noun; "lassen is een" and "санитарных норм и"
    are the same thing in two other languages. Trimming until both ends hold
    a content word is what makes one rule serve all seven.
    """
    if _is_elided_tail(candidate):
        return ""
    words = candidate.strip(" -–—.·•*").split()
    if language in ELIDING_LANGUAGES:
        words = [_drop_elision(word) for word in words]
    edges = _edge_words(language)

    heads = _head_nouns()

    def droppable(word: str) -> bool:
        folded = fold(word)
        return not folded or folded in edges or _is_numeral(folded, language)

    while words and droppable(words[-1]) and not (len(words) > 1 and fold(words[-1]) in heads):
        words.pop()
    while words and droppable(words[0]):
        words.pop(0)
    if words and language in ("uk", "ru") and len(words) > 1:
        # A leading infinitive belongs to the introducer, not to the
        # requirement: "умение работать с пароконвектоматом".
        if fold(words[0]).endswith(_SLAVIC_INFINITIVE_ENDINGS):
            words.pop(0)
            while words and droppable(words[0]):
                words.pop(0)
    return " ".join(words)


ADJECTIVE_ENDINGS: dict[str, tuple[str, ...]] = {
    # Endings that mark a word as describing a noun rather than being one.
    # Checked only against a single word the gazetteer left behind, never
    # against a phrase, so they can afford to be broad.
    "en": ("al", "ial", "ual", "ive", "ous", "ed"),
    "es": ("al", "ales", "ivo", "iva", "ivos", "ivas", "oso", "osa", "era", "ero"),
    "fr": ("el", "elle", "al", "ale", "aux", "elles", "if", "ive", "ives"),
    "nl": ("eel", "ele", "isch", "ische", "ig", "ige"),
}
"""Per language, because the same letters mean different things: Spanish
"maquinaria" and French "plaies" are nouns an advert really is asking for,
while "financiera" and "industriel" only describe the noun beside them."""


def _is_leftover_modifier(before: str, after: str, language: str) -> bool:
    """Whether what the gazetteer left behind only describes what it took.

    English and the Romance languages put the adjective after the noun, and
    the noun is the half the gazetteer knows: "cocina profesional",
    "contabilidad financiera", "nettoyage industriel", "professional kitchen".
    The skill was recorded, the noun removed as already explained, and the
    adjective came back as a requirement of its own -- eleven of them across
    eighty-two adverts, every one a word no recruiter asked for.

    So a single word left over after the gazetteer took part of the phrase is
    dropped when it is shaped like an adjective. Shaped, not merely single:
    "soins des plaies" leaves "plaies" and "maquinaria de limpieza" leaves
    "maquinaria", which are the wound care and the machines the advert wants.

    A word capitalised where the language does not capitalise nouns is kept
    whatever its ending: "Docker Swarm" leaves "Swarm", a product rather than
    a description of one. German is left alone entirely -- it capitalises
    every noun, and its leftovers ("Vorgaben", "Richtlinien") are already
    known framing words.
    """
    if after == before or " " in after:
        return False
    if language in NOUN_CAPITALISING_LANGUAGES or after[:1].isupper():
        return False
    return fold(after).endswith(ADJECTIVE_ENDINGS.get(language, ()))


def _is_bare_modifier(candidate: str, language: str) -> bool:
    """Whether a single-word candidate is an adjective with no noun.

    Two languages give this away by morphology and one by case. Russian and
    Ukrainian mark adjectives with an ending; German marks every noun with a
    capital letter, so a lowercase word standing alone is not one. Both
    situations arise the same way: the noun the adjective belonged to was a
    lexicon hit and got removed, leaving its modifier behind as a
    requirement of its own.
    """
    if " " in candidate:
        return False
    folded = fold(candidate)
    if language in ("uk", "ru"):
        return len(folded) >= 6 and folded.endswith(_SLAVIC_ADJECTIVE_ENDINGS)
    if language in NOUN_CAPITALISING_LANGUAGES:
        return candidate[:1].islower()
    return False


def _drop_covered_words(candidate: str, covered: set[str]) -> str:
    """Remove the words a lexicon match already explained.

    Filtering has to work on whole original words, not on folded tokens:
    folding splits "IT-Systemen" into two tokens while ``str.split`` keeps it
    as one, and zipping the two lists together sliced characters out of the
    middle of words -- "Elektronik" came back as "ektronik".
    """
    kept = []
    for word in candidate.split():
        tokens = fold(word).split()
        if tokens and all(token in covered for token in tokens):
            continue
        kept.append(word)
    return " ".join(kept)


def _collect(
    candidate: str,
    covered: set[str],
    found: list[Candidate],
    language: str,
    weight: int,
) -> None:
    candidate = _trim(candidate, language)
    if len(candidate) < MIN_TERM_LENGTH:
        return
    folded = fold(candidate)
    if not folded or folded in STOPWORDS:
        return
    # Language names are declined ("Німецька", "Deutschkenntnisse"), so the
    # exact-match stoplist misses them; their levels are read by the typed
    # extractor and the bare name would be a duplicate requirement.
    if any(word.startswith(_LANGUAGE_PREFIXES) for word in folded.split()):
        return
    # Words a lexicon match already explained are removed rather than the
    # whole phrase: "HACCP-Richtlinien" collapses to nothing and disappears,
    # while "underwater welding" keeps the half the gazetteer does not know.
    before = candidate
    candidate = _trim(_drop_covered_words(candidate, covered), language)
    folded = fold(candidate)
    if len(candidate) < MIN_TERM_LENGTH or not folded:
        return
    if _is_leftover_modifier(before, candidate, language):
        return
    if all(word in STOPWORDS for word in folded.split()):
        return
    if _is_bare_modifier(candidate, language):
        return
    if any(fold(existing.text) == folded for existing in found):
        return
    found.append(Candidate(candidate, weight))
