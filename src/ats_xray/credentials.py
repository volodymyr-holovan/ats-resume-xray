"""Education, experience, language level and licence: the requirements a job
advert states as facts about a person rather than as skills.

These are worth separating from the skill gazetteer because they compare
differently. A skill either appears or it does not. A degree is a *level*,
and a Master satisfies an advert asking for a Bachelor while the reverse is
not true. Years of experience are a number to meet. A language is a CEFR
level to reach. Treating all four as keywords would report "Bachelor" as
missing from a CV that says "Master of Science", which is exactly the kind of
wrong that makes a match report untrustworthy.

Every vocabulary here is keyed by language and read through
:func:`langid.merge_for`, which returns the document's own language plus
English. Reading all seven at once was not merely wasteful, it was wrong:
Spanish "diploma" sits inside German "Diplomatie", and Dutch "promotie"
means a doctorate in Dutch and a sales campaign in German.

German phrasing is the most developed of the seven because German adverts
are formulaic enough to read reliably: they say "abgeschlossenes Studium der
Informatik oder vergleichbare Qualifikation" in nearly those words, every
time.
"""

import re
from dataclasses import dataclass
from datetime import date

from .langid import detect_language, merge_for
from .normalize import fold

# --------------------------------------------------------------------------
# Education
# --------------------------------------------------------------------------

EDUCATION_RANK = {
    "ausbildung": 1,
    "bachelor": 2,
    "master": 3,
    "doctorate": 4,
}
"""Ordered so a comparison is a comparison. "Studium" without a named degree
maps to bachelor: an advert asking for "ein abgeschlossenes Studium" is
satisfied by a Bachelor, and reading it as anything higher would invent a
requirement the employer did not state."""

EDUCATION_MARKERS_BY_LANGUAGE: dict[str, dict[str, tuple[str, ...]]] = {
    "de": {
        # Bare "Promotion" is left out on purpose. It means a doctorate in a
        # German advert and an advertising campaign in an English one, and
        # the cost of guessing wrong is inventing a doctorate requirement.
        "doctorate": ("doktortitel", "doktorgrad", "doktorarbeit", "abgeschlossene promotion", "promovierter", "promovierte", "promoviert", "dr rer nat"),
        "master": ("masterabschluss", "masterstudium", "master of science", "master of arts", "master of engineering", "masterarbeit", "m sc", "m.sc", "m.a", "m eng", "m.eng", "msc", "diplomarbeit", "diplomstudium", "diplomingenieur", "diplominformatiker", "dipl ing", "dipl inf", "diplom"),
        "bachelor": ("bachelorabschluss", "bachelorstudium", "bachelor of science", "bachelor of arts", "bachelor of engineering", "bachelorarbeit", "b sc", "b.sc", "b.a", "b eng", "b.eng", "bsc", "bachelor", "hochschulabschluss", "hochschulstudium", "fachhochschulstudium", "universitaetsabschluss", "akademischer abschluss", "abgeschlossenes studium", "abgeschlossenem studium", "studium der", "studium im bereich", "studium im fachbereich", "technisches studium"),
        "ausbildung": ("abgeschlossene ausbildung", "abgeschlossener ausbildung", "abgeschlossene berufsausbildung", "berufsausbildung", "ausbildung als", "ausbildung im bereich", "fachinformatiker", "fachinformatikerin", "it-systemkaufmann", "informatikkaufmann", "techniker", "meisterbrief", "ihk-abschluss"),
    },
    "en": {
        "doctorate": ("phd", "ph d", "doctorate", "doctoral degree"),
        "master": ("master degree", "masters degree", "graduate degree", "master of science", "master of arts"),
        "bachelor": ("bachelors degree", "bachelor degree", "university degree", "academic degree", "degree in", "completed degree", "higher education"),
        "ausbildung": ("vocational training", "apprenticeship", "completed training", "trade certificate"),
    },
    "es": {
        "doctorate": ("doctorado",),
        "master": ("master en", "maestria", "postgrado"),
        "bachelor": ("estudios de", "estudios universitarios", "titulacion", "grado en", "licenciatura", "diplomatura"),
        "ausbildung": ("formacion profesional", "ciclo formativo"),
    },
    "nl": {
        "doctorate": ("promotie", "gepromoveerd"),
        "master": ("masteropleiding", "master in"),
        "bachelor": ("afgeronde opleiding", "hbo-opleiding", "wo-opleiding", "bacheloropleiding", "hbo werk- en denkniveau"),
        "ausbildung": ("mbo-opleiding", "mbo werk- en denkniveau", "beroepsopleiding"),
    },
    "fr": {
        "doctorate": ("doctorat",),
        "master": ("master en", "mastere", "bac+5"),
        "bachelor": ("diplome en", "licence en", "bac+3", "formation superieure"),
        "ausbildung": ("cap ou bep", "apprentissage", "formation professionnelle"),
    },
    "uk": {
        "doctorate": ("кандидат наук", "доктор наук", "докторська"),
        "master": ("магістр", "магістратура"),
        "bachelor": ("вища освіта", "вищу освіту", "бакалавр", "бакалаврат"),
        "ausbildung": ("профтехосвіта", "середня спеціальна", "фаховий молодший бакалавр"),
    },
    "ru": {
        "doctorate": ("кандидат наук", "доктор наук", "докторская"),
        "master": ("магистр", "магистратура"),
        "bachelor": ("высшее образование", "бакалавр", "бакалавриат"),
        "ausbildung": ("среднее специальное", "профессиональное образование"),
    },
}

_BARE_MASTER = re.compile(r"\bmaster\b")
_MASTER_NOT_A_DEGREE = ("scrum", "product", "data", "db", "postmaster", "webmaster")
"""A Scrum Master is not a Master's degree. The word only counts as a degree
when nothing in front of it says otherwise."""

EQUIVALENT_BY_LANGUAGE: dict[str, tuple[str, ...]] = {
    "de": ("vergleichbare qualifikation", "vergleichbarer qualifikation", "vergleichbare ausbildung", "vergleichbarer abschluss", "vergleichbaren abschluss", "vergleichbare berufserfahrung", "oder vergleichbar", "oder vergleichbares", "gleichwertige qualifikation", "aehnliche qualifikation"),
    "en": ("or equivalent", "equivalent experience", "equivalent qualification", "comparable qualification"),
    "es": ("o titulacion equivalente", "o equivalente"),
    "nl": ("of vergelijkbaar", "of gelijkwaardig"),
    "fr": ("ou equivalent", "ou formation equivalente"),
    "uk": ("або еквівалентна", "або рівноцінна"),
    "ru": ("или эквивалентное", "или равноценное"),
}
"""Phrases that turn a hard degree requirement into a preference. Common
enough in German adverts that ignoring them would overstate how many
candidates are excluded."""

WAIVED_BY_LANGUAGE: dict[str, tuple[str, ...]] = {
    "de": ("auch ohne studium", "ohne abgeschlossenes studium", "kein studium erforderlich", "quereinsteiger willkommen", "quereinsteiger", "quereinsteigerinnen"),
    "en": ("career changers", "no degree required", "degree not required"),
    "es": ("sin titulacion", "no se requiere titulacion"),
    "nl": ("zonder diploma", "geen diploma vereist"),
    "fr": ("sans diplome", "reconversion"),
    "uk": ("без вищої освіти",),
    "ru": ("без высшего образования",),
}

STUDY_FIELDS_BY_LANGUAGE: dict[str, dict[str, tuple[str, ...]]] = {
    "de": {
        "informatik": ("informatik", "wirtschaftsinformatik", "medieninformatik", "angewandte informatik", "technische informatik", "softwaretechnik", "informationstechnik"),
        "engineering": ("elektrotechnik", "ingenieurwesen", "maschinenbau", "mechatronik", "nachrichtentechnik"),
        "mathematics": ("mathematik", "statistik", "physik", "naturwissenschaft", "naturwissenschaften"),
        "business": ("betriebswirtschaft", "betriebswirtschaftslehre", "bwl", "wirtschaftswissenschaft", "wirtschaftswissenschaften"),
    },
    "en": {
        "informatik": ("computer science", "software engineering", "information technology", "informatics"),
        "engineering": ("engineering", "mechanical engineering", "electrical engineering"),
        "mathematics": ("mathematics", "physics", "data science", "natural sciences"),
        "business": ("business administration", "economics", "finance"),
    },
    "es": {
        "informatik": ("informatica", "ingenieria informatica"),
        "engineering": ("ingenieria", "ingenieria industrial"),
        "mathematics": ("matematicas", "fisica", "ciencias"),
        "business": ("empresariales", "administracion de empresas", "economia"),
    },
    "nl": {
        "informatik": ("informatica", "computerwetenschappen"),
        "engineering": ("werktuigbouwkunde", "elektrotechniek", "techniek"),
        "mathematics": ("wiskunde", "natuurkunde"),
        "business": ("bedrijfskunde", "economie"),
    },
    "fr": {
        "informatik": ("informatique", "genie logiciel"),
        "engineering": ("ingenierie", "genie mecanique", "genie electrique"),
        "mathematics": ("mathematiques", "physique", "sciences"),
        "business": ("gestion", "economie", "commerce"),
    },
    "uk": {
        "informatik": ("інформатик", "комп'ютерн"),
        "engineering": ("інженер",),
        "mathematics": ("математик", "фізик"),
        "business": ("економік", "менеджмент"),
    },
    "ru": {
        "informatik": ("информатик", "компьютерн"),
        "engineering": ("инженер",),
        "mathematics": ("математик", "физик"),
        "business": ("эконом", "менеджмент"),
    },
}

MIN_COMPOUND_MARKER = 5
"""Below this length a marker is an abbreviation, and abbreviations turn up
inside longer words by accident: "bsc" sits in "A**bsc**hlussstärke". Only
markers long enough to be words in their own right may match inside a German
compound."""

WORD_ONLY_MARKERS = frozenset({"diplom", "bachelor", "master", "techniker", "promotie"})
"""Markers that must match as whole words despite being long enough not to.
Each is the beginning of an unrelated word somewhere: Diplomatie,
Bachelorette, Mastermind, Elektrotechniker as a job title rather than a
qualification."""


def _contains(folded: str, marker: str) -> bool:
    """Whether a folded text states this marker.

    Long single-word markers match inside a word, because that is how German
    compounds work: "Informatik" has to be found inside
    "Wirtschaftsinformatik".

    Everything else must align with word boundaries. Two real failures came
    from skipping that: "m sc" was found in "zu**m sc**hichtdienst", turning
    a shift-work requirement into a Master's degree, and "bsc" in
    "A**bsc**hlussstärke" invented a Bachelor's out of a sales skill.
    """
    if " " in marker or len(marker) < MIN_COMPOUND_MARKER or marker in WORD_ONLY_MARKERS:
        return re.search(rf"\b{re.escape(marker)}\b", folded) is not None
    return marker in folded


def _merged_levels(language: str) -> dict[str, tuple[str, ...]]:
    merged: dict[str, list[str]] = {level: [] for level in EDUCATION_RANK}
    for code in (language, "en"):
        for level, markers in EDUCATION_MARKERS_BY_LANGUAGE.get(code, {}).items():
            merged[level].extend(markers)
    return {level: tuple(markers) for level, markers in merged.items()}


def _merged_fields(language: str) -> dict[str, tuple[str, ...]]:
    merged: dict[str, list[str]] = {}
    for code in (language, "en"):
        for field, markers in STUDY_FIELDS_BY_LANGUAGE.get(code, {}).items():
            merged.setdefault(field, []).extend(markers)
    return {field: tuple(markers) for field, markers in merged.items()}


@dataclass(frozen=True)
class EducationFact:
    level: str
    field: str | None = None
    equivalent_accepted: bool = False
    evidence: str = ""

    @property
    def rank(self) -> int:
        return EDUCATION_RANK.get(self.level, 0)


def find_education(text: str, language: str | None = None) -> EducationFact | None:
    """Highest education level stated in ``text``.

    Highest rather than first: a CV listing an apprenticeship and then a
    degree has the degree, and an advert saying "Bachelor oder Master" is
    satisfied by the Bachelor it also named.
    """
    folded = fold(text)
    if not folded:
        return None
    language = language or detect_language(text)

    best: tuple[int, str] | None = None
    for level, markers in _merged_levels(language).items():
        for marker in markers:
            if _contains(folded, marker):
                rank = EDUCATION_RANK[level]
                if best is None or rank > best[0]:
                    best = (rank, marker)
                break

    # Checked as a candidate rather than only as a fallback: "Master's degree
    # in engineering" also contains "degree in", which on its own reads as a
    # Bachelor and would understate the requirement.
    if _has_degree_master(folded) and (best is None or best[0] < EDUCATION_RANK["master"]):
        best = (EDUCATION_RANK["master"], "master")

    if best is None:
        return None

    level = next(name for name, rank in EDUCATION_RANK.items() if rank == best[0])
    return EducationFact(
        level=level,
        field=find_study_field(folded, language),
        equivalent_accepted=any(
            _contains(folded, phrase) for phrase in merge_for(EQUIVALENT_BY_LANGUAGE, language)
        ),
        evidence=best[1],
    )


def _has_degree_master(folded: str) -> bool:
    for match in _BARE_MASTER.finditer(folded):
        before = folded[max(0, match.start() - 24) : match.start()]
        if not any(word in before for word in _MASTER_NOT_A_DEGREE):
            return True
    return False


def find_study_field(folded_text: str, language: str = "en") -> str | None:
    for field, markers in _merged_fields(language).items():
        if any(_contains(folded_text, marker) for marker in markers):
            return field
    return None


def education_waived(text: str, language: str | None = None) -> bool:
    language = language or detect_language(text)
    folded = fold(text)
    return any(_contains(folded, phrase) for phrase in merge_for(WAIVED_BY_LANGUAGE, language))


# --------------------------------------------------------------------------
# Years of experience
# --------------------------------------------------------------------------

_YEARS_NUMERIC = re.compile(
    r"(?:mindestens|mind\.?|min\.?|wenigstens|at least|über|mehr als|more than|al menos|minstens|au moins|щонайменше|не менше|не менее)?\s*"
    r"(\d{1,2})\s*(?:\+|bis|-|–|to|a|tot|à|до)?\s*(?:\d{1,2})?\s*"
    r"(?:jahre?n?|jahres|years?|jhr|anos|años|jaar|ans|années|рок\w*|лет|года)",
    re.IGNORECASE,
)
_EXPERIENCE_WORD = re.compile(
    r"erfahrung|experience|praxis|experiencia|ervaring|expérience|досвід|опыт", re.IGNORECASE
)

VAGUE_EXPERIENCE_BY_LANGUAGE: dict[str, tuple[tuple[str, int], ...]] = {
    "de": (("langjährige", 5), ("mehrjährige", 3), ("fundierte berufserfahrung", 3), ("einschlägige berufserfahrung", 2), ("erste berufserfahrung", 1), ("erste erfahrung", 1)),
    "en": (("several years", 3), ("extensive experience", 5), ("solid experience", 3), ("first experience", 1), ("some experience", 1)),
    "es": (("amplia experiencia", 5), ("varios anos", 3), ("primera experiencia", 1)),
    "nl": (("ruime ervaring", 5), ("meerdere jaren", 3), ("eerste ervaring", 1)),
    "fr": (("longue experience", 5), ("plusieurs annees", 3), ("premiere experience", 1)),
    "uk": (("багаторічний досвід", 5), ("кількарічний досвід", 3)),
    "ru": (("многолетний опыт", 5), ("несколько лет", 3), ("первый опыт", 1)),
}
"""Adverts often state a duration without a number. These are the
conventional readings; they are approximations and the report says so."""


SPELLED_NUMBERS: dict[str, dict[str, int]] = {
    "de": {"ein": 1, "eine": 1, "einem": 1, "zwei": 2, "drei": 3, "vier": 4, "fünf": 5, "sechs": 6, "sieben": 7, "acht": 8, "zehn": 10},
    "en": {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "ten": 10},
    "es": {"un": 1, "uno": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5},
    "nl": {"een": 1, "twee": 2, "drie": 3, "vier": 4, "vijf": 5},
    "fr": {"un": 1, "deux": 2, "trois": 3, "quatre": 4, "cinq": 5},
    "uk": {"один": 1, "два": 2, "три": 3, "чотири": 4, "п'ять": 5},
    "ru": {"один": 1, "два": 2, "три": 3, "четыре": 4, "пять": 5},
}
"""Adverts write small numbers as words as often as digits: "mindestens
zwei Jahre Berufserfahrung" is as common as "mindestens 2 Jahre"."""

_YEAR_WORD = re.compile(
    r"(jahre?n?|years?|anos|años|jaar|ans|années|рок\w*|лет|года)", re.IGNORECASE
)


def _spelled_years(text: str, language: str) -> int | None:
    """A spelled-out number sitting immediately before the word "years"."""
    match = _YEAR_WORD.search(text)
    if match is None:
        return None
    before = fold(text[max(0, match.start() - 24) : match.start()]).split()
    if not before:
        return None
    numbers: dict[str, int] = {}
    for code in (language, "en"):
        numbers.update({fold(word): value for word, value in SPELLED_NUMBERS.get(code, {}).items()})
    return numbers.get(before[-1])


def find_required_years(text: str, language: str | None = None) -> int | None:
    """Years of experience an advert line asks for, if it asks for any.

    A number only counts when the same line also talks about experience:
    "3 Jahre" on its own is as likely to be a project duration or a contract
    term as a requirement.
    """
    if not _EXPERIENCE_WORD.search(text):
        return None

    match = _YEARS_NUMERIC.search(text)
    if match:
        return int(match.group(1))

    language = language or detect_language(text)

    spelled = _spelled_years(text, language)
    if spelled is not None:
        return spelled

    folded = fold(text)
    for phrase, years in merge_for(VAGUE_EXPERIENCE_BY_LANGUAGE, language):
        if fold(phrase) in folded:
            return years
    return None


# --------------------------------------------------------------------------
# Experience actually present in a CV
# --------------------------------------------------------------------------

_OPEN_ENDED = (
    "heute", "present", "aktuell", "today", "now", "jetzt", "laufend", "ongoing",
    "current", "actualidad", "heden", "нині", "настоящее время",
)
_MONTH_YEAR = r"(\d{1,2})[./](\d{4})"
_YEAR_ONLY = r"(\d{4})"
_RANGE_SEPARATOR = r"\s*(?:-|–|—|bis|to|until|hasta|tot|до)\s*"

_DATE_RANGE = re.compile(
    rf"(?:{_MONTH_YEAR}|{_YEAR_ONLY}){_RANGE_SEPARATOR}"
    rf"(?:{_MONTH_YEAR}|{_YEAR_ONLY}|({'|'.join(_OPEN_ENDED)}))",
    re.IGNORECASE,
)
_SINCE = re.compile(
    rf"(?:seit|since|desde|sinds|depuis|з|с)\s+(?:{_MONTH_YEAR}|{_YEAR_ONLY})", re.IGNORECASE
)

MIN_PLAUSIBLE_YEAR = 1960


def find_experience_months(text: str, today: date | None = None) -> int:
    """Total months covered by the date ranges in ``text``.

    Overlapping entries are merged rather than added: someone who worked part
    time while studying has not lived through both spans twice, and summing
    them would produce a CV claiming more years than the person has been
    alive.
    """
    today = today or date.today()
    spans: list[tuple[int, int]] = []

    for match in _DATE_RANGE.finditer(text):
        # Groups: 1-2 start month/year, 3 start year-only,
        #         4-5 end month/year, 6 end year-only, 7 open-ended word.
        start = _to_month_index(match.group(1), match.group(2), match.group(3))
        if start is None:
            continue
        if match.group(7):
            end = today.year * 12 + today.month
        else:
            end = _to_month_index(match.group(4), match.group(5), match.group(6), end_of_year=True)
        if end is None or end < start:
            continue
        spans.append((start, end))

    for match in _SINCE.finditer(text):
        start = _to_month_index(match.group(1), match.group(2), match.group(3))
        if start is not None:
            spans.append((start, today.year * 12 + today.month))

    return _merged_length(spans)


def _to_month_index(month, year, year_only, end_of_year: bool = False) -> int | None:
    if year_only:
        value = int(year_only)
        if value < MIN_PLAUSIBLE_YEAR:
            return None
        return value * 12 + (12 if end_of_year else 1)
    if month and year:
        month_value, year_value = int(month), int(year)
        if not 1 <= month_value <= 12 or year_value < MIN_PLAUSIBLE_YEAR:
            return None
        return year_value * 12 + month_value
    return None


def _merged_length(spans: list[tuple[int, int]]) -> int:
    if not spans:
        return 0
    merged: list[list[int]] = []
    for start, end in sorted(spans):
        if merged and start <= merged[-1][1] + 1:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return sum(end - start + 1 for start, end in merged)


# --------------------------------------------------------------------------
# Languages
# --------------------------------------------------------------------------

CEFR_RANK = {"a1": 1, "a2": 2, "b1": 3, "b2": 4, "c1": 5, "c2": 6}

LANGUAGE_NAMES_BY_LANGUAGE: dict[str, dict[str, tuple[str, ...]]] = {
    # Each document names languages in its own language: a Spanish advert
    # asks for "aleman", never for "Deutsch".
    "de": {"de": ("deutsch", "deutschkenntnisse"), "en": ("englisch", "englischkenntnisse"), "fr": ("franzoesisch",), "es": ("spanisch",), "nl": ("niederlaendisch",), "it": ("italienisch",), "pl": ("polnisch",), "uk": ("ukrainisch",), "ru": ("russisch",)},
    "en": {"de": ("german",), "en": ("english",), "fr": ("french",), "es": ("spanish",), "nl": ("dutch",), "it": ("italian",), "pl": ("polish",), "uk": ("ukrainian",), "ru": ("russian",)},
    "es": {"de": ("aleman",), "en": ("ingles",), "fr": ("frances",), "es": ("espanol",), "nl": ("holandes", "neerlandes"), "it": ("italiano",), "pl": ("polaco",), "uk": ("ucraniano",), "ru": ("ruso",)},
    "nl": {"de": ("duits",), "en": ("engels",), "fr": ("frans",), "es": ("spaans",), "nl": ("nederlands",), "it": ("italiaans",), "pl": ("pools",), "uk": ("oekraiens",), "ru": ("russisch",)},
    "fr": {"de": ("allemand",), "en": ("anglais",), "fr": ("francais",), "es": ("espagnol",), "nl": ("neerlandais",), "it": ("italien",), "pl": ("polonais",), "uk": ("ukrainien",), "ru": ("russe",)},
    "uk": {"de": ("німецьк",), "en": ("англійськ",), "fr": ("французьк",), "es": ("іспанськ",), "nl": ("нідерландськ",), "it": ("італійськ",), "pl": ("польськ",), "uk": ("українськ",), "ru": ("російськ",)},
    "ru": {"de": ("немецк",), "en": ("английск",), "fr": ("французск",), "es": ("испанск",), "nl": ("голландск", "нидерландск"), "it": ("итальянск",), "pl": ("польск",), "uk": ("украинск",), "ru": ("русск",)},
}

DESCRIPTORS_BY_LANGUAGE: dict[str, tuple[tuple[str, str], ...]] = {
    "de": (("muttersprache", "c2"), ("muttersprachlich", "c2"), ("verhandlungssicher", "c1"), ("fliessend", "c1"), ("sehr gute", "c1"), ("sehr gut", "c1"), ("gute", "b2"), ("gut", "b2"), ("solide", "b2"), ("grundkenntnisse", "a2")),
    "en": (("native", "c2"), ("business fluent", "c1"), ("fluent", "c1"), ("excellent", "c1"), ("good", "b2"), ("working knowledge", "b2"), ("basic", "a2")),
    "es": (("nativo", "c2"), ("fluido", "c1"), ("alto", "c1"), ("bueno", "b2"), ("basico", "a2")),
    "nl": (("moedertaal", "c2"), ("vloeiend", "c1"), ("uitstekend", "c1"), ("goede", "b2"), ("goed", "b2"), ("basis", "a2")),
    "fr": (("langue maternelle", "c2"), ("courant", "c1"), ("excellent", "c1"), ("bonne", "b2"), ("bon", "b2"), ("notions", "a2")),
    "uk": (("рідна", "c2"), ("вільне володіння", "c1"), ("вільно", "c1"), ("впевнено", "b2"), ("добре", "b2"), ("базов", "a2"), ("початков", "a2")),
    "ru": (("родной", "c2"), ("свободное владение", "c1"), ("свободно", "c1"), ("уверенно", "b2"), ("хорошо", "b2"), ("базов", "a2"), ("начальн", "a2")),
}
"""Adverts rarely print a CEFR level; they print an adjective. The mapping is
the conventional one recruiters use, and it is approximate by nature:
"verhandlungssicher" is a judgement, not a test result."""

_CEFR_PATTERN = re.compile(r"\b([abc][12])\b", re.IGNORECASE)
_WINDOW_BEFORE = 48
_WINDOW_AFTER = 48
"""German writes the level in front of the language ("verhandlungssichere
Deutschkenntnisse") and CVs write it behind ("Deutsch - B2"), so both sides
have to be read. The nearest level wins, which is what keeps "Deutsch C1,
Englisch B2" from giving both languages a C1."""


@dataclass(frozen=True)
class LanguageFact:
    language: str
    level: str
    evidence: str = ""

    @property
    def rank(self) -> int:
        return CEFR_RANK.get(self.level, 0)


def _names_for(language: str) -> dict[str, tuple[str, ...]]:
    merged: dict[str, list[str]] = {}
    for code in (language, "en"):
        for spoken, names in LANGUAGE_NAMES_BY_LANGUAGE.get(code, {}).items():
            merged.setdefault(spoken, []).extend(fold(name) for name in names)
    return {spoken: tuple(dict.fromkeys(names)) for spoken, names in merged.items()}


def find_languages(text: str, language: str | None = None) -> list[LanguageFact]:
    """Language levels stated in ``text``, one entry per language.

    Reads a window around each language name rather than the whole text, so
    "Deutsch C1, Englisch B2" does not give both languages the higher level.
    Where a language appears more than once, the highest level found wins.
    """
    language = language or detect_language(text)
    folded = fold(text)
    names = _names_for(language)
    descriptors = merge_for(DESCRIPTORS_BY_LANGUAGE, language)
    best: dict[str, LanguageFact] = {}

    for code, spellings in names.items():
        for name in spellings:
            for match in re.finditer(rf"\b{re.escape(name)}", folded):
                level = _nearest_level(folded, match.start(), match.end(), code, names, descriptors)
                if level is None:
                    continue
                evidence = folded[max(0, match.start() - 20) : match.end() + 20].strip()
                fact = LanguageFact(code, level, evidence)
                if code not in best or fact.rank > best[code].rank:
                    best[code] = fact

    return sorted(best.values(), key=lambda f: f.language)


def _other_language_positions(text: str, exclude: str, names: dict) -> list[tuple[int, int]]:
    return [
        (match.start(), match.end())
        for code, spellings in names.items()
        if code != exclude
        for name in spellings
        for match in re.finditer(rf"\b{re.escape(name)}", text)
    ]


def _nearest_level(folded, start, end, code, names, descriptors) -> str | None:
    before = folded[max(0, start - _WINDOW_BEFORE) : start]
    after = folded[end : end + _WINDOW_AFTER]

    # Trim each side at the next language named, so "fließende
    # Englischkenntnisse, Deutsch" leaves German with no level rather than
    # borrowing English's.
    ahead = _other_language_positions(after, code, names)
    if ahead:
        after = after[: min(s for s, _ in ahead)]
    behind = _other_language_positions(before, code, names)
    if behind:
        before = before[max(e for _, e in behind) :]

    candidates: list[tuple[int, int, str]] = []
    for match in _CEFR_PATTERN.finditer(after):
        candidates.append((match.start(), -2, match.group(1).lower()))
    for match in _CEFR_PATTERN.finditer(before):
        candidates.append((len(before) - match.end(), -2, match.group(1).lower()))

    for descriptor, level in descriptors:
        folded_descriptor = fold(descriptor)
        index = after.find(folded_descriptor)
        if index != -1:
            candidates.append((index, -len(folded_descriptor), level))
        index = before.rfind(folded_descriptor)
        if index != -1:
            candidates.append(
                (len(before) - (index + len(folded_descriptor)), -len(folded_descriptor), level)
            )

    if not candidates:
        return None
    # Nearest first; on a tie the longer marker wins, so "sehr gute" is not
    # read as the "gute" sitting inside it.
    candidates.sort(key=lambda item: (item[0], item[1]))
    return candidates[0][2]


def language_required_without_level(text: str, language: str | None = None) -> list[str]:
    """Languages named with no level attached anywhere near them.

    An advert that just says "Deutsch und Englisch" is still stating a
    requirement; reporting nothing at all would hide it.
    """
    language = language or detect_language(text)
    folded = fold(text)
    names = _names_for(language)
    descriptors = merge_for(DESCRIPTORS_BY_LANGUAGE, language)
    named: list[str] = []

    for code, spellings in names.items():
        for name in spellings:
            match = re.search(rf"\b{re.escape(name)}", folded)
            if match and _nearest_level(folded, match.start(), match.end(), code, names, descriptors) is None:
                named.append(code)
                break
    return named


# --------------------------------------------------------------------------
# Driving licence
# --------------------------------------------------------------------------

LICENCE_MARKERS = (
    "fuehrerschein", "fahrerlaubnis", "pkw-fuehrerschein",
    "driving licence", "driving license", "drivers license", "driver s license",
    "carnet de conducir", "permis de conduire", "rijbewijs",
    "водійське посвідчення", "водительские права",
)
_LICENCE_CLASS = re.compile(
    r"(?:klasse|class|categoria|categorie|категорі\w*|категори\w*)\s*([a-z]{1,2}\d{0,2}[a-z]?)\b",
    re.IGNORECASE,
)


def find_licence(text: str) -> str | None:
    """The driving licence class an advert asks for, or ``"B"`` when it asks
    for a licence without naming one -- class B is what "Führerschein" means
    when nothing else is said."""
    folded = fold(text)
    if not any(fold(marker) in folded for marker in LICENCE_MARKERS):
        return None
    match = _LICENCE_CLASS.search(folded)
    return match.group(1).upper() if match else "B"
