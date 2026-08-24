"""Education, experience, language level and licence: the requirements a
job advert states as facts about a person rather than as skills.

These are worth separating from the skill gazetteer because they compare
differently. A skill either appears or it does not. A degree is a *level*,
and a Master satisfies an advert asking for a Bachelor while the reverse is
not true. Years of experience are a number to meet. A language is a CEFR
level to reach. Treating all four as keywords would report "Bachelor" as
missing from a CV that says "Master of Science", which is exactly the kind
of wrong that makes a match report untrustworthy.

German advert phrasing drives most of the decisions here, because German
adverts are formulaic enough to read reliably: they say "abgeschlossenes
Studium der Informatik oder vergleichbare Qualifikation" in nearly those
words, every time.
"""

import re
from dataclasses import dataclass
from datetime import date

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
"""Ordered so a comparison is a comparison. "studium" without a named degree
maps to bachelor: an advert asking for "ein abgeschlossenes Studium" is
satisfied by a Bachelor, and reading it as anything higher would invent a
requirement the employer did not state."""

EDUCATION_MARKERS: dict[str, tuple[str, ...]] = {
    "doctorate": (
        # Bare "Promotion" is left out on purpose. It means a doctorate in a
        # German advert and an advertising campaign in an English one, and
        # the cost of guessing wrong is inventing a doctorate requirement.
        "doktortitel",
        "doktorgrad",
        "doktorarbeit",
        "abgeschlossene promotion",
        "promovierter",
        "promovierte",
        "promoviert",
        "phd",
        "ph d",
        "dr rer nat",
        "doctorate",
        "doctoral degree",
    ),
    "master": (
        "masterabschluss",
        "masterstudium",
        "master of science",
        "master of arts",
        "master of engineering",
        "masterarbeit",
        # Both spacings: folding keeps a dot inside a word ("m.sc") but turns
        # the one in "M. Sc." into a space.
        "m sc",
        "m.sc",
        "m.a",
        "m eng",
        "m.eng",
        "msc",
        "diplom",
        "diplomarbeit",
        "dipl ing",
        "dipl inf",
        "master degree",
        "masters degree",
        "graduate degree",
    ),
    "bachelor": (
        "bachelorabschluss",
        "bachelorstudium",
        "bachelor of science",
        "bachelor of arts",
        "bachelor of engineering",
        "bachelorarbeit",
        "b sc",
        "b.sc",
        "b.a",
        "b eng",
        "b.eng",
        "bsc",
        "bachelor",
        "hochschulabschluss",
        "hochschulstudium",
        "fachhochschulstudium",
        "universitaetsabschluss",
        "akademischer abschluss",
        "abgeschlossenes studium",
        "abgeschlossenem studium",
        "studium der",
        "studium im bereich",
        "studium im fachbereich",
        "technisches studium",
        "bachelors degree",
        "university degree",
        "academic degree",
        "degree in",
    ),
    "ausbildung": (
        "abgeschlossene ausbildung",
        "abgeschlossener ausbildung",
        "abgeschlossene berufsausbildung",
        "berufsausbildung",
        "ausbildung als",
        "ausbildung im bereich",
        "fachinformatiker",
        "fachinformatikerin",
        "it-systemkaufmann",
        "informatikkaufmann",
        "techniker",
        "meisterbrief",
        "ihk-abschluss",
        "vocational training",
        "apprenticeship",
        "completed training",
    ),
}

_BARE_MASTER = re.compile(r"\bmaster\b")
_MASTER_NOT_A_DEGREE = ("scrum", "product", "data", "db", "postmaster", "webmaster")
"""A Scrum Master is not a Master's degree. The word only counts as a degree
when nothing in front of it says otherwise."""

EQUIVALENT_ACCEPTED = (
    "vergleichbare qualifikation",
    "vergleichbarer qualifikation",
    "vergleichbare ausbildung",
    "vergleichbarer abschluss",
    "vergleichbaren abschluss",
    "vergleichbare berufserfahrung",
    "oder vergleichbar",
    "oder vergleichbares",
    "gleichwertige qualifikation",
    "aehnliche qualifikation",
    "or equivalent",
    "equivalent experience",
    "equivalent qualification",
    "comparable qualification",
)
"""Phrases that turn a hard degree requirement into a preference. Common
enough in German adverts that ignoring them would overstate how many
candidates are excluded."""

EDUCATION_WAIVED = (
    "auch ohne studium",
    "ohne abgeschlossenes studium",
    "kein studium erforderlich",
    "quereinsteiger willkommen",
    "quereinsteiger",
    "quereinsteigerinnen",
    "career changers",
    "no degree required",
)

STUDY_FIELDS: dict[str, tuple[str, ...]] = {
    "informatik": (
        "informatik",
        "wirtschaftsinformatik",
        "medieninformatik",
        "angewandte informatik",
        "technische informatik",
        "softwaretechnik",
        "software engineering",
        "computer science",
        "information technology",
        "informationstechnik",
    ),
    "engineering": (
        "elektrotechnik",
        "ingenieurwesen",
        "maschinenbau",
        "mechatronik",
        "nachrichtentechnik",
        "engineering",
    ),
    "mathematics": (
        "mathematik",
        "statistik",
        "physik",
        "naturwissenschaft",
        "naturwissenschaften",
        "data science",
        "mathematics",
        "physics",
    ),
    "business": (
        "betriebswirtschaft",
        "betriebswirtschaftslehre",
        "bwl",
        "wirtschaftswissenschaft",
        "wirtschaftswissenschaften",
        "business administration",
        "economics",
    ),
}


@dataclass(frozen=True)
class EducationFact:
    level: str
    field: str | None = None
    equivalent_accepted: bool = False
    evidence: str = ""

    @property
    def rank(self) -> int:
        return EDUCATION_RANK.get(self.level, 0)


def find_education(text: str) -> EducationFact | None:
    """Highest education level stated in ``text``.

    Highest rather than first: a CV listing an apprenticeship and then a
    degree has the degree, and an advert saying "Bachelor oder Master" is
    satisfied by the Bachelor it also named.
    """
    folded = fold(text)
    if not folded:
        return None

    best: tuple[int, str] | None = None
    for level, markers in EDUCATION_MARKERS.items():
        for marker in markers:
            if marker in folded:
                rank = EDUCATION_RANK[level]
                if best is None or rank > best[0]:
                    best = (rank, marker)
                break

    if best is None and _has_degree_master(folded):
        best = (EDUCATION_RANK["master"], "master")

    if best is None:
        return None

    level = next(name for name, rank in EDUCATION_RANK.items() if rank == best[0])
    return EducationFact(
        level=level,
        field=find_study_field(folded),
        equivalent_accepted=any(phrase in folded for phrase in EQUIVALENT_ACCEPTED),
        evidence=best[1],
    )


def _has_degree_master(folded: str) -> bool:
    for match in _BARE_MASTER.finditer(folded):
        before = folded[max(0, match.start() - 24) : match.start()]
        if not any(word in before for word in _MASTER_NOT_A_DEGREE):
            return True
    return False


def find_study_field(folded_text: str) -> str | None:
    for field, markers in STUDY_FIELDS.items():
        if any(marker in folded_text for marker in markers):
            return field
    return None


def education_waived(text: str) -> bool:
    folded = fold(text)
    return any(phrase in folded for phrase in EDUCATION_WAIVED)


# --------------------------------------------------------------------------
# Years of experience
# --------------------------------------------------------------------------

_YEARS_NUMERIC = re.compile(
    r"(?:mindestens|mind\.?|min\.?|wenigstens|at least|ueber|über|mehr als|more than)?\s*"
    r"(\d{1,2})\s*(?:\+|bis|-|–|to)?\s*(?:\d{1,2})?\s*"
    r"(?:jahre?n?|jahres|years?|jhr)",
    re.IGNORECASE,
)
_EXPERIENCE_WORD = re.compile(r"erfahrung|experience|praxis", re.IGNORECASE)

VAGUE_EXPERIENCE = (
    ("langjaehrige", 5),
    ("langjährige", 5),
    ("mehrjaehrige", 3),
    ("mehrjährige", 3),
    ("several years", 3),
    ("fundierte berufserfahrung", 3),
    ("einschlaegige berufserfahrung", 2),
    ("einschlägige berufserfahrung", 2),
    ("erste berufserfahrung", 1),
    ("erste erfahrung", 1),
    ("first experience", 1),
)
"""German adverts often state a duration without a number. These are the
conventional readings; they are approximations and the report says so."""


def find_required_years(text: str) -> int | None:
    """Years of experience an advert line asks for, if it asks for any.

    A number only counts when the same line also talks about experience:
    "3 Jahre" on its own is as likely to be a project duration or a
    contract term as a requirement.
    """
    if not _EXPERIENCE_WORD.search(text):
        return None

    match = _YEARS_NUMERIC.search(text)
    if match:
        return int(match.group(1))

    folded = fold(text)
    for phrase, years in VAGUE_EXPERIENCE:
        if fold(phrase) in folded:
            return years
    return None


# --------------------------------------------------------------------------
# Experience actually present in a CV
# --------------------------------------------------------------------------

_OPEN_ENDED = ("heute", "present", "aktuell", "today", "now", "jetzt", "laufend", "ongoing", "current")
_MONTH_YEAR = r"(\d{1,2})[./](\d{4})"
_YEAR_ONLY = r"(\d{4})"
_RANGE_SEPARATOR = r"\s*(?:-|–|—|bis|to|until)\s*"

_DATE_RANGE = re.compile(
    rf"(?:{_MONTH_YEAR}|{_YEAR_ONLY}){_RANGE_SEPARATOR}"
    rf"(?:{_MONTH_YEAR}|{_YEAR_ONLY}|({'|'.join(_OPEN_ENDED)}))",
    re.IGNORECASE,
)
_SINCE = re.compile(rf"(?:seit|since)\s+(?:{_MONTH_YEAR}|{_YEAR_ONLY})", re.IGNORECASE)

MIN_PLAUSIBLE_YEAR = 1960


def find_experience_months(text: str, today: date | None = None) -> int:
    """Total months covered by the date ranges in ``text``.

    Overlapping entries are merged rather than added: someone who worked
    part time while studying has not lived through both spans twice, and
    summing them would produce a CV claiming more years than the person
    has been alive.
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


def _to_month_index(month: str | None, year: str | None, year_only: str | None, end_of_year: bool = False) -> int | None:
    if year_only:
        value = int(year_only)
        if value < MIN_PLAUSIBLE_YEAR:
            return None
        return value * 12 + (12 if end_of_year else 1)
    if month and year:
        month_value = int(month)
        year_value = int(year)
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

LANGUAGE_NAMES: dict[str, tuple[str, ...]] = {
    "de": ("deutsch", "deutschkenntnisse", "german"),
    "en": ("englisch", "englischkenntnisse", "english"),
    "fr": ("franzoesisch", "french"),
    "es": ("spanisch", "spanish"),
    "nl": ("niederlaendisch", "dutch"),
    "it": ("italienisch", "italian"),
    "pl": ("polnisch", "polish"),
    "uk": ("ukrainisch", "ukrainian"),
    "ru": ("russisch", "russian"),
}

DESCRIPTOR_TO_CEFR = (
    ("muttersprache", "c2"),
    ("muttersprachlich", "c2"),
    ("native", "c2"),
    ("verhandlungssicher", "c1"),
    ("verhandlungssichere", "c1"),
    ("fliessend", "c1"),
    ("fluent", "c1"),
    ("sehr gute", "c1"),
    ("sehr gut", "c1"),
    ("business fluent", "c1"),
    ("gute", "b2"),
    ("gut", "b2"),
    ("good", "b2"),
    ("solide", "b2"),
    ("grundkenntnisse", "a2"),
    ("basic", "a2"),
)
"""German adverts rarely print a CEFR level; they print an adjective. The
mapping is the conventional one recruiters use, and it is approximate by
nature: "verhandlungssicher" is a judgement, not a test result."""

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


def find_languages(text: str) -> list[LanguageFact]:
    """Language levels stated in ``text``, one entry per language.

    Reads a window around each language name rather than the whole text,
    so "Deutsch C1, Englisch B2" does not give both languages the higher
    level. Where a language appears more than once, the highest level
    found wins.
    """
    folded = fold(text)
    best: dict[str, LanguageFact] = {}

    for code, names in LANGUAGE_NAMES.items():
        for name in names:
            for match in re.finditer(rf"\b{re.escape(name)}", folded):
                level = _nearest_level(folded, match.start(), match.end(), code)
                if level is None:
                    continue
                evidence = folded[max(0, match.start() - 20) : match.end() + 20].strip()
                fact = LanguageFact(code, level, evidence)
                if code not in best or fact.rank > best[code].rank:
                    best[code] = fact

    return sorted(best.values(), key=lambda f: f.language)


def _other_language_positions(text: str, exclude: str) -> list[tuple[int, int]]:
    return [
        (match.start(), match.end())
        for code, names in LANGUAGE_NAMES.items()
        if code != exclude
        for name in names
        for match in re.finditer(rf"\b{re.escape(name)}", text)
    ]


def _trim_after(text: str, exclude: str) -> str:
    """Cut at the first other language named, so "Englisch - C1" sitting
    behind "Deutsch" does not become German's level."""
    positions = _other_language_positions(text, exclude)
    return text[: min(start for start, _ in positions)] if positions else text


def _trim_before(text: str, exclude: str) -> str:
    """Same idea reading backwards: keep only what follows the last other
    language named, so "fließende Englischkenntnisse, Deutsch" leaves
    German with no level rather than borrowing English's."""
    positions = _other_language_positions(text, exclude)
    return text[max(end for _, end in positions) :] if positions else text


def _nearest_level(folded: str, start: int, end: int, code: str) -> str | None:
    before = folded[max(0, start - _WINDOW_BEFORE) : start]
    after = folded[end : end + _WINDOW_AFTER]

    after = _trim_after(after, code)
    before = _trim_before(before, code)

    candidates: list[tuple[int, int, str]] = []

    for match in _CEFR_PATTERN.finditer(after):
        candidates.append((match.start(), -2, match.group(1).lower()))
    for match in _CEFR_PATTERN.finditer(before):
        candidates.append((len(before) - match.end(), -2, match.group(1).lower()))

    for descriptor, level in DESCRIPTOR_TO_CEFR:
        index = after.find(descriptor)
        if index != -1:
            candidates.append((index, -len(descriptor), level))
        index = before.rfind(descriptor)
        if index != -1:
            candidates.append((len(before) - (index + len(descriptor)), -len(descriptor), level))

    if not candidates:
        return None
    # Nearest first; on a tie the longer marker wins, so "sehr gute" is not
    # read as the "gute" sitting inside it.
    candidates.sort(key=lambda item: (item[0], item[1]))
    return candidates[0][2]


def language_required_without_level(text: str) -> list[str]:
    """Languages named with no level attached anywhere near them.

    An advert that just says "Deutsch und Englisch" is still stating a
    requirement; reporting nothing at all would hide it.
    """
    folded = fold(text)
    named: list[str] = []
    for code, names in LANGUAGE_NAMES.items():
        for name in names:
            match = re.search(rf"\b{re.escape(name)}", folded)
            if match and _nearest_level(folded, match.start(), match.end(), code) is None:
                named.append(code)
                break
    return named


# --------------------------------------------------------------------------
# Driving licence
# --------------------------------------------------------------------------

LICENCE_MARKERS = (
    "fuehrerschein",
    "fahrerlaubnis",
    "pkw-fuehrerschein",
    "driving licence",
    "driving license",
    "drivers license",
    "driver s license",
)
# Licence classes mix letters and digits: B, BE, C1, C1E. A letters-only
# class matches nothing on "Klasse C1" and silently falls back to "B".
_LICENCE_CLASS = re.compile(r"(?:klasse|class)\s*([a-z]{1,2}\d{0,2}[a-z]?)\b", re.IGNORECASE)


def find_licence(text: str) -> str | None:
    """The driving licence class an advert asks for, or ``"B"`` when it asks
    for a licence without naming one -- class B is what "Führerschein" means
    when nothing else is said."""
    folded = fold(text)
    if not any(marker in folded for marker in LICENCE_MARKERS):
        return None
    match = _LICENCE_CLASS.search(folded)
    if match:
        return match.group(1).upper()
    return "B"
