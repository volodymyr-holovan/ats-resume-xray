"""Pull requirement keywords out of an advert the lexicon does not know.

A curated lexicon is accurate and finite. It cannot cover every trade, every
certificate and every piece of equipment a job might name, and an advert for
a profession nobody thought to add would otherwise produce an empty
requirements list -- which is worse than a rough one, because the reader has
nothing to correct.

Two cheap signals do most of the work:

*German capitalises its nouns.* Every requirement worth extracting from a
German advert is a noun, and almost nothing else in the sentence is
capitalised. That is a better part-of-speech tagger than anything that would
fit in this project's dependencies. It is applied to other languages too,
where it is weaker but still finds product and certificate names.

*Every language announces requirements with the same few phrases.*
"Kenntnisse in", "Erfahrung mit", "experience with", "conocimiento de",
"досвід роботи з". What follows one of those is a requirement by
construction, in any of the seven languages the app speaks.

The hard part is not finding candidates but rejecting them. A German bullet
starts with a capital letter whatever word is there, so "Abgeschlossene",
"Gute" and "Mindestens" all look like nouns; the stoplist below is what
keeps them out. Everything that survives is still a guess, and the interface
shows it in an editable list before anything is scored.
"""

import re

from .credentials import LANGUAGE_NAMES_BY_LANGUAGE
from .langid import merge_for
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
    "technische", "technisches", "technischer", "direkter", "direkte",
    "moderne", "modernes", "hochwertiges", "attraktive", "gründliche",
    "abwechslungsreiches", "innovativem", "wichtige", "verschiedene",
    # Infinitives that open a German task bullet. They are capitalised there
    # by sentence position and look exactly like nouns.
    "führen", "betreuen", "durchführen", "erstellen", "pflegen", "unterstützen",
    "bearbeiten", "planen", "koordinieren", "überwachen", "sicherstellen",
    "mitwirken", "umsetzen", "analysieren", "beraten", "dokumentieren",
    "organisieren", "verwalten", "entwickeln", "warten", "prüfen", "begleiten",
    "steuern", "leiten", "abstimmen", "erfassen", "auswerten", "montieren",
    # The people a job serves are not a skill.
    "bewohner", "patienten", "patient", "gäste", "gast", "klienten", "nutzer",
    "anwender", "besucher", "bewerber", "schüler", "teilnehmer", "personen",
    "menschen", "bürger", "mandanten", "gemeinde", "kinder", "jugendliche",
    # What is left over when a compound's first half was a lexicon hit:
    # "HACCP-Vorgaben" must not come back as a requirement called "Vorgaben".
    "vorgabe", "vorgaben", "regelungen", "bestimmungen", "grundsätze",
    "kriterien", "aspekte", "inhalte", "punkte", "verfahren", "methoden",
    "maßnahmen", "abläufe", "vorschriften", "unterlagen", "dokumente",
    # Nouns that describe taking part in work rather than any skill. German
    # task bullets are built out of these: "Mitarbeit bei der Umsetzung der
    # Vorgaben" names nothing a candidate could have.
    "mitarbeit", "mitwirkung", "umsetzung", "übernahme", "unterstützung",
    "erstellung", "bearbeitung", "abwicklung", "sicherstellung", "gestaltung",
    "verantwortung", "posten", "einsatzort", "schwerpunkt", "schwerpunkte",
    "geräte", "gerät", "einstieg", "einarbeitung", "anfertigung",
    "optimierung", "installation", "infrastruktur", "komponenten",
)

_FRAMING_WORDS = (
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
    "bachelor", "master", "diplom", "promotion", "degree",
    # Company and posting boilerplate.
    "unternehmen", "firma", "arbeitgeber", "stelle", "position", "team", "teams",
    "mitarbeiter", "mitarbeiterinnen", "kollegen", "kunden", "kunde", "bewerbung",
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
    # Spanish
    "conocimiento", "conocimientos", "experiencia", "estudios", "titulacion",
    "perfil", "requisitos", "funciones", "ofrecemos", "anos", "capacidad",
    "dominio", "nivel", "buen", "buena", "alto", "alta", "imprescindible",
    "valorable", "deseable", "empresa", "puesto", "equipo",
    # Dutch
    "kennis", "ervaring", "opleiding", "profiel", "vereisten", "taken",
    "jaar", "jaren", "goede", "sterke", "afgeronde", "vloeiend", "pre",
    "vaardigheden", "bedrijf", "functie", "werkzaamheden",
    # French
    "connaissance", "connaissances", "experience", "diplome", "missions",
    "exigences", "bonne", "bonnes", "maitrise", "souhaite", "atout",
    "entreprise", "poste", "equipe", "competences",
    # Ukrainian
    "знання", "досвід", "освіта", "вища", "вищу", "профіль", "вимоги",
    "обов", "язки", "роки", "років", "рівень", "володіння", "бажано",
    "обовязково", "компанія", "посада", "команда", "навички",
    # Russian
    "знание", "опыт", "образование", "высшее", "профиль", "требования",
    "обязанности", "годы", "лет", "уровень", "владение", "желательно",
    "обязательно", "компания", "должность", "команда", "навыки",
    # Slavic bullets open with these the way German ones open with
    # "Abgeschlossene": they quantify the requirement, they are not it.
    "щонайменше", "не менше", "принаймні", "профільна", "профільне",
    "закінчена", "закінчене", "чинна", "чинне", "впевнене", "готовність",
    "бажання", "уміння", "вміння", "не менее", "профильное", "профильная",
    "законченное", "действующая", "уверенное", "готовность", "желание",
    "умение", "высшее", "среднее", "начальное",
)

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
    ),
    "en": (
        r"experience\s+(?:with|in|of|as)",
        r"knowledge\s+of",
        r"proficiency\s+(?:in|with)",
        r"familiarity\s+with",
        r"skills?\s+in",
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
    ),
    "nl": (
        r"ervaring\s+(?:met|in)",
        r"kennis\s+van",
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
    "uk": (
        r"досвід\s+(?:роботи\s+)?(?:з|у|в|із)",
        r"знання(?:\s+(?:з|у|в))?",
        r"володіння",
        r"вміння",
        r"навички(?:\s+(?:з|у|в))?",
    ),
    "ru": (
        r"опыт\s+(?:работы\s+)?(?:с|в|со)",
        r"знание(?:\s+(?:в|по))?",
        r"владение",
        r"умение",
        r"навыки(?:\s+(?:в|по))?",
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
            + r"([\w\-]+(?:\s+[\w\-]+){0,%d})" % (MAX_PHRASE_WORDS - 1),
            re.IGNORECASE | re.UNICODE,
        )
        _PATTERN_CACHE[language] = cached
    return cached


_PATTERN_CACHE: dict[str, re.Pattern] = {}

_CAPITALISED = re.compile(r"(\w*[^\W\d_]\w*)", re.UNICODE)
_SPLIT_ON = re.compile(r"\s+(?:und|oder|sowie|and|or|y|en|et|та|и|или)\s+|[,;:()/]", re.IGNORECASE)


def extract_terms(line: str, language: str = "en") -> list[str]:
    """Requirement keywords in one advert line, best guesses first.

    Words already explained by a lexicon match are left out: they are
    reported as the skill they belong to, and repeating them as loose nouns
    would show the same requirement twice.
    """
    _, covered = find_skills_and_covered(line)
    found: list[str] = []

    for match in _introduced_pattern(language).finditer(line):
        for candidate in _SPLIT_ON.split(match.group(1)):
            _collect(candidate, covered, found)

    if not _is_shouted(line):
        for word in _CAPITALISED.findall(line):
            if word[:1].isupper():
                _collect(word, covered, found)

    return found


def _is_shouted(line: str) -> bool:
    letters = [ch for ch in line if ch.isalpha()]
    if len(letters) < 3:
        return False
    return sum(ch.isupper() for ch in letters) / len(letters) >= UPPERCASE_LINE_RATIO


def _is_elided(word: str) -> bool:
    """Whether a word is the tail of an elided German compound.

    "Fehlersuche und -behebung" means Fehlersuche and Fehlerbehebung; the
    hyphen stands in for the head. Reporting "behebung" on its own names
    nothing, and the reader cannot trace it back to the advert.
    """
    return word.lstrip(" ").startswith(("-", "–", "—"))


def _trim(candidate: str) -> str:
    """Drop framing words from both ends of a captured phrase.

    "Pflegedokumentation sind zwingend" is the phrase pattern doing its job
    and then running past the noun; the requirement is the first word.
    """
    if _is_elided(candidate):
        return ""
    words = candidate.strip(" -–—.·•*").split()
    while words and fold(words[-1]) in STOPWORDS:
        words.pop()
    while words and fold(words[0]) in STOPWORDS:
        words.pop(0)
    return " ".join(words)


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


def _collect(candidate: str, covered: set[str], found: list[str]) -> None:
    candidate = _trim(candidate)
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
    candidate = _drop_covered_words(candidate, covered)
    folded = fold(candidate)
    if len(candidate) < MIN_TERM_LENGTH or not folded:
        return
    if all(word in STOPWORDS for word in folded.split()):
        return
    if any(fold(existing) == folded for existing in found):
        return
    found.append(candidate)
