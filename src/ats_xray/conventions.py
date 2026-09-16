"""Things a CV says that a recruiter in its country does not expect.

Every other detector in this project asks whether software can read the
file. These ask the question a parser never will: having read it, does the
CV follow the conventions of the place it is going?

A German recruiter who finds volunteering listed under Berufserfahrung reads
it as a job -- Berufserfahrung means paid employment -- and then finds out it
was not, which is worse than never having been told. A date range that ends
before it starts is read by an applicant tracking system as nothing at all,
and the years of experience it was meant to prove silently disappear from
the filter. Neither is a parsing fault; both cost the application.

Conventions are national, and this reads language, not nationality. A
German-language CV is taken to be going to a German-speaking employer and a
Ukrainian one to a Ukrainian employer, because that is the only signal the
file carries. Each detector names the languages it applies to and nothing
fires outside them: where the research found a convention to be a
preference rather than a rule, the detector stays silent rather than
exporting German expectations to a Dutch CV.

None of this counts against the parse-readiness score. See
``rule.CONVENTION``.
"""

import re
from dataclasses import dataclass
from datetime import date

from .credentials import DateSpan, find_date_spans, find_experience_months
from .langid import detect_language
from .normalize import fold
from .sections import find_section_headers, split_into_sections

# --------------------------------------------------------------------------
# Shared
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class ConventionFinding:
    evidence_key: str
    params: dict
    severity: str


def _month_index(day: date) -> int:
    return day.year * 12 + day.month


def _format_month(index: int) -> str:
    year, month = divmod(index, 12)
    if month == 0:
        year, month = year - 1, 12
    return f"{month:02d}/{year}"


def _section_by_line(text: str) -> list[str]:
    """The section each line belongs to, as the section splitter sees it.

    Lines before the first recognised heading belong to ``"preamble"``; a
    heading line belongs to the section it opens.
    """
    lines = text.splitlines()
    owner = ["preamble"] * len(lines)
    headers = find_section_headers(text)
    for position, header in enumerate(headers):
        stop = headers[position + 1]["line_index"] if position + 1 < len(headers) else len(lines)
        for index in range(header["line_index"], stop):
            owner[index] = header["section"]
    return owner


def _shorten(line: str, limit: int = 120) -> str:
    line = " ".join(line.split())
    return line if len(line) <= limit else line[: limit - 1].rstrip() + "…"


# --------------------------------------------------------------------------
# Volunteering listed as employment
# --------------------------------------------------------------------------

VOLUNTEERING_LANGUAGES = frozenset({"de", "uk"})
"""Where volunteering belongs in its own section as a rule, not a preference.

German career guidance is consistent that an Ehrenamt does not replace
Berufserfahrung and goes in its own section after experience and education;
Ukrainian guidance says the same of волонтерство unless it was the person's
full-time occupation. Dutch, Spanish, French, English and Russian guidance
all accept volunteering under work experience when it is relevant or paid
experience is thin, so a CV in those languages is left alone. See
research_sources.md#cv-volunteering."""

_VOLUNTEER_MARKERS: dict[str, tuple[str, ...]] = {
    "de": ("ehrenamt", "freiwilligenarbeit", "freiwillige helfer", "freiwilliger helfer",
           "freiwillige mitarbeit", "unentgeltlich", "volunteer"),
    "uk": ("волонтер", "на громадських засадах", "безоплатн"),
}

_VOLUNTEER_EXCEPTIONS: dict[str, tuple[str, ...]] = {
    "de": ("freiwilliges soziales jahr", "freiwilliges oekologisches jahr",
           "bundesfreiwilligendienst", "freiwilliger wehrdienst", "fsj", "foej", "bfd"),
    "uk": (),
}
"""Formal services that happen to carry the word "freiwillig" and are not
volunteering in the sense the convention means. An FSJ or a
Bundesfreiwilligendienst is a full-time placement with pay and social
insurance, and German guidance places it under Berufserfahrung whenever it
reads as practical work. Flagging it would tell a school leaver to move the
only real work they have out of their experience."""

def _mentions(padded_folded: str, phrase: str) -> bool:
    """Whether a phrase occurs, as whole words when it is an abbreviation.

    "fsj" inside a longer word is not the Freiwilliges Soziales Jahr; a full
    phrase like "bundesfreiwilligendienst" can only ever be itself.
    """
    if len(phrase) <= 4:
        return f" {phrase} " in padded_folded
    return phrase in padded_folded


_PHRASE = re.compile(r"[,;:|/()·•–—-]")
_LEADING_NUMBERS = re.compile(r"^(?:\d+\s+)+")


def _opens_a_phrase(line: str, markers: tuple[str, ...]) -> bool:
    """Whether a marker starts a phrase here, rather than sitting inside one.

    Mentioning volunteering is not the same as filing volunteering under
    employment, and in both German and Ukrainian the difference is
    grammatical. The candidate's own unpaid role opens its phrase --
    "Ehrenamtliche Tätigkeit, Tafel Hamburg e.V.", "Волонтер, Карітас" --
    behind nothing but a date, a bullet or a separator. Other people's
    volunteering is governed by the noun in front of it: "Schulung
    ehrenamtlicher Helfer" is a duty of a paid job, "Координація роботи
    волонтерів" likewise, and "Verein zur Förderung ehrenamtlicher Arbeit" is
    an employer's name. Matching the bare word reported all of them, on
    fourteen of eighty-one real CVs that had put their volunteering exactly
    where the convention asks for it.

    No offset is ever taken into folded text. ``fold`` expands umlauts and
    drops punctuation, so it does not preserve length and a position found in
    the folded string points somewhere else in the raw one. The raw line is
    cut into phrases first, and each phrase folded on its own.
    """
    for span in find_date_spans(line):
        line = line.replace(span.raw, " ")
    for phrase in _PHRASE.split(line):
        opening = _LEADING_NUMBERS.sub("", fold(phrase))
        if any(opening.startswith(marker) for marker in markers):
            return True
    return False


def _dates_above(rows: list[str], index: int) -> list[int]:
    """The date line an undated volunteer line belongs to, if it has one.

    CVs put the role on the line under the dates as often as beside them:
    "2016 - 2020  Tafel Hamburg e.V." then "Ehrenamtliche Helferin". When the
    marker line carries no date itself, the entry's date is the nearest one
    just above it.
    """
    if find_date_spans(rows[index]):
        return []
    for above in range(index - 1, max(index - 3, -1), -1):
        if find_date_spans(rows[above]):
            return [above]
    return []


CAREER_STARTER_MONTHS = 24
"""Below this much dated experience, the German exception applies.

A career starter may list relevant volunteering under Berufserfahrung,
because for them it is the practical experience there is. The finding still
appears -- the reader should know the convention -- but as low rather than
medium, and the advice says the exception exists."""


def find_volunteering_in_experience(text: str, language: str) -> ConventionFinding | None:
    if language not in VOLUNTEERING_LANGUAGES:
        return None
    experience = split_into_sections(text).get("experience")
    if not experience:
        return None

    markers = _VOLUNTEER_MARKERS[language]
    exceptions = _VOLUNTEER_EXCEPTIONS[language]
    rows = experience.splitlines()
    lines, volunteer_rows = [], set()
    for index, line in enumerate(rows):
        folded = f" {fold(line)} "
        if any(_mentions(folded, exception) for exception in exceptions):
            continue
        if _opens_a_phrase(line, markers):
            lines.append(_shorten(line))
            volunteer_rows.add(index)
            volunteer_rows.update(_dates_above(rows, index))
    if not lines:
        return None

    # Paid experience only. Counting the whole section let the volunteering
    # prove its own seniority: a starter with a year of paid work and three
    # years coaching a sports club read as four years' experience, and was
    # denied the exception that exists for exactly them.
    paid = "\n".join(row for index, row in enumerate(rows) if index not in volunteer_rows)
    starter = find_experience_months(paid) < CAREER_STARTER_MONTHS
    return ConventionFinding(
        evidence_key="evidence_volunteering_starter" if starter else "evidence_volunteering",
        params={"text": "; ".join(lines[:2])},
        severity="low" if starter else "medium",
    )


# --------------------------------------------------------------------------
# Gaps nobody explained
# --------------------------------------------------------------------------

GAP_LANGUAGES = frozenset({"de"})
"""The lückenloser Lebenslauf is a German expectation. Elsewhere a gap is a
question for the interview; in a German CV an unexplained one is read as
something being hidden."""

GAP_MONTHS = 4
"""Shortest gap worth reporting.

German guidance calls anything past two months a gap and treats three to
four as the point where it needs an explanation, with eight to ten weeks
harmless. Four is the top of that range on purpose: dates on a CV are
imprecise -- a year on its own covers twelve months -- and a threshold at
the bottom of the range would report gaps that are really rounding."""

SERIOUS_GAP_MONTHS = 7
"""From here the gap is reported as medium rather than low."""

GRACE_AFTER_EDUCATION_MONTHS = 6
"""Looking for a first job after finishing a qualification takes time, and
German guidance allows about six months of it without comment."""


def find_unexplained_gap(text: str, language: str, today: date | None = None) -> ConventionFinding | None:
    if language not in GAP_LANGUAGES:
        return None
    today = today or date.today()
    now = _month_index(today)
    owners = _section_by_line(text)
    spans = find_date_spans(text)

    # A timeline with a broken entry cannot be judged for gaps. The entry
    # "03/2021 - 01/2020" is a job with a typo in it, and leaving it out
    # does not leave out a job that never existed -- it opens a hole where
    # the job was. On a real CV that turned one mistyped digit into a
    # sixty-nine-month gap reported beside the date error that caused it.
    # The dates are reported; the gaps wait until they are fixed.
    if any(span.end is not None and span.end < span.start for span in spans):
        return None

    intervals: list[tuple[int, int, str]] = []
    for span in spans:
        end = now if span.open_ended else span.end
        if span.start > now:
            continue  # a future date is its own finding, not a gap
        intervals.append((span.start, min(end, now), owners[span.line] if span.line < len(owners) else ""))
    if len(intervals) < 2:
        return None

    intervals.sort()
    merged: list[list] = []
    for start, end, section in intervals:
        if merged and start <= merged[-1][1] + 1:
            if end > merged[-1][1]:
                merged[-1][1], merged[-1][2] = end, section
        else:
            merged.append([start, end, section])

    gaps: list[tuple[int, int]] = []
    for previous, following in zip(merged, merged[1:]):
        gaps.append(_gap(previous, following[0]))
    if merged[-1][1] < now:
        gaps.append(_gap(merged[-1], now + 1))

    # Every gap long enough to need a line, and the longest one named. All
    # of them are counted because fixing the one in the evidence and leaving
    # two more is how the reader would otherwise act on this.
    reportable = [(first, last) for first, last in gaps if last - first + 1 >= GAP_MONTHS]
    if not reportable:
        return None
    first, last = max(reportable, key=lambda gap: gap[1] - gap[0])
    length = last - first + 1
    return ConventionFinding(
        evidence_key="evidence_gap",
        params={
            "count": len(reportable),
            "start": _format_month(first),
            "end": _format_month(last),
            "months": length,
        },
        severity="medium" if length >= SERIOUS_GAP_MONTHS else "low",
    )


def _gap(previous: list, next_start: int) -> tuple[int, int]:
    """The empty months between one covered stretch and the next.

    A stretch that ended with education gets its grace period taken off the
    front, so a normal job search after a degree is never reported.
    """
    first = previous[1] + 1
    if previous[2] == "education":
        first += GRACE_AFTER_EDUCATION_MONTHS
    return first, next_start - 1


# --------------------------------------------------------------------------
# Dates that cannot be true
# --------------------------------------------------------------------------

FUTURE_MARGIN_MONTHS = 24
"""How far past today a date may sit before it is read as a typo.

A signed contract can start next quarter and a fixed-term one can end next
year, so a near-future date is ordinary. Two years out on a job that
already appears in the CV is not a plan; it is 2052 typed for 2025."""

_FUTURE_EXEMPT_SECTIONS = frozenset({"education", "certifications"})
"""An expected graduation three years away is how every student writes
their degree."""


def find_impossible_dates(text: str, today: date | None = None) -> ConventionFinding | None:
    today = today or date.today()
    limit = _month_index(today) + FUTURE_MARGIN_MONTHS
    owners = _section_by_line(text)
    spans = find_date_spans(text)

    backwards = [span for span in spans if span.end is not None and span.end < span.start]
    if backwards:
        return ConventionFinding(
            evidence_key="evidence_date_backwards",
            params={"text": backwards[0].raw},
            severity="medium",
        )

    future = [
        span for span in spans
        if (span.line >= len(owners) or owners[span.line] not in _FUTURE_EXEMPT_SECTIONS)
        and (span.start > limit or (span.end is not None and span.end > limit))
    ]
    if future:
        return ConventionFinding(
            evidence_key="evidence_date_future",
            params={"text": future[0].raw},
            severity="medium",
        )
    return None


# --------------------------------------------------------------------------
# Sentences about "I"
# --------------------------------------------------------------------------

FIRST_PERSON_LANGUAGES = frozenset({"de", "en"})
"""German guidance on the tabellarischer Lebenslauf and US career-office
guidance agree: entries are written as fragments, not as sentences about
oneself. Both make the same exception for a short profile at the top."""

_GERMAN_I = re.compile(r"\b[Ii]ch\b")
"""Case-sensitive on purpose: "ICH" is the International Council for
Harmonisation, and "ICH-GCP" is on every clinical-research CV in Germany."""

_ENGLISH_I = re.compile(r"\bI(?:'m|'ve|'d|'ll|\s+([a-z]+))")
_ENGLISH_NOT_A_VERB = frozenset({"and", "or", "to", "through"})


def _first_person_count(line: str, language: str) -> int:
    if language == "de":
        return len(_GERMAN_I.findall(line))
    count = 0
    for match in _ENGLISH_I.finditer(line):
        if match.group(1) in _ENGLISH_NOT_A_VERB:
            continue  # "Phase I and II", "Levels I to III"
        before = line[: match.start()].split()
        previous = before[-1] if before else ""
        if previous[:1].isupper() and previous.isalpha():
            continue  # "Phase I in", "Level I certification": a numeral
        count += 1
    return count


_PROFILE_SECTIONS = frozenset({"preamble", "summary"})
"""Where first-person writing is allowed: the few lines under the name, and
a section labelled as a profile."""

MIN_FIRST_PERSON = 2
"""One "ich" can be a quotation or a job title. Two is a habit."""


def find_first_person(text: str, language: str) -> ConventionFinding | None:
    if language not in FIRST_PERSON_LANGUAGES:
        return None
    owners = _section_by_line(text)
    count, first = 0, ""
    for index, line in enumerate(text.splitlines()):
        if index >= len(owners) or owners[index] in _PROFILE_SECTIONS:
            continue
        found = _first_person_count(line, language)
        if found and not first:
            first = line
        count += found
    if count < MIN_FIRST_PERSON:
        return None
    return ConventionFinding(
        evidence_key="evidence_first_person",
        params={"count": count, "text": _shorten(first)},
        severity="low",
    )


# --------------------------------------------------------------------------
# Personal details the law made unnecessary
# --------------------------------------------------------------------------

PERSONAL_DETAIL_LANGUAGES = frozenset({"de"})

_LABEL_END = r"(?:\s*:|\s+[\-–—]\s|\s{2,}|\t|\s*$)"
"""What separates a label from its value: a colon, a dash with space on both
sides, the run of spaces a two-column layout leaves behind, or nothing at all
when the value sits on the next line.

A dash only counts with spaces around it. German joins compounds with a
hyphen, and a bare one matched "Kinder- und Jugendhilfe" as a Kinder field
and "Mutter-Kind-Station" as a parent -- a youth-welfare office and a
maternity ward, reported as personal details."""

_OUTDATED_LABELS: dict[str, re.Pattern] = {
    # These words open a line only as the personal-data field.
    "Konfession": re.compile(r"^\s*(?:konfession|religionszugehörigkeit)\b"),
    "Familienstand": re.compile(r"^\s*familienstand\b"),
    # These open lines for other reasons too, so they must look like a label.
    "Religion": re.compile(rf"^\s*religion{_LABEL_END}"),
    "Kinder": re.compile(rf"^\s*kinder{_LABEL_END}"),
    "Eltern": re.compile(rf"^\s*(?:vater|mutter|eltern|(?:name|beruf) de[sr] (?:vaters|mutter)){_LABEL_END}"),
}
"""Matched only as labels at the start of a line.

The words themselves are everywhere. "Evangelisches Krankenhaus" and
"Katholisches Klinikum" are employers; "Religion und Ethik" is a teaching
subject; "Kinder- und Jugendhilfe" is a field; "Mutter-Kind-Station" is a
ward. What is outdated is the personal-data field, and the field is
recognisable by being a label -- which is also why this reads the line as
written rather than folded: folding turns the colon that marks a label into
a space."""


def find_outdated_personal_details(text: str, language: str) -> ConventionFinding | None:
    if language not in PERSONAL_DETAIL_LANGUAGES:
        return None
    found = []
    for line in text.splitlines():
        lowered = line.lower()
        for label, pattern in _OUTDATED_LABELS.items():
            if label not in found and pattern.search(lowered):
                found.append(label)
    if not found:
        return None
    return ConventionFinding(
        evidence_key="evidence_outdated_details",
        params={"text": ", ".join(found)},
        severity="low",
    )


# --------------------------------------------------------------------------
# Oldest entry first
# --------------------------------------------------------------------------

ORDER_LANGUAGES = frozenset({"de", "en"})
"""Reverse chronological order is the standard in German CVs and the format
it came from in the US: the reader looks at the top for what the candidate
does now."""

MIN_ORDERED_ENTRIES = 3


def find_oldest_first(text: str, language: str) -> ConventionFinding | None:
    if language not in ORDER_LANGUAGES:
        return None
    experience = split_into_sections(text).get("experience")
    if not experience:
        return None
    spans = [span for span in find_date_spans(experience)
             if span.end is None or span.end >= span.start]
    if len(spans) < MIN_ORDERED_ENTRIES:
        return None
    starts = [span.start for span in spans]
    rises = sum(1 for before, after in zip(starts, starts[1:]) if after > before)
    falls = sum(1 for before, after in zip(starts, starts[1:]) if after < before)
    if falls or rises < MIN_ORDERED_ENTRIES - 1:
        return None
    return ConventionFinding(
        evidence_key="evidence_oldest_first",
        params={"first": spans[0].raw, "last": spans[-1].raw},
        severity="low",
    )


# --------------------------------------------------------------------------
# Everything at once
# --------------------------------------------------------------------------


def analyze_conventions(
    text: str, today: date | None = None, language: str | None = None
) -> dict[str, ConventionFinding | None]:
    """Every convention check for one CV, keyed by the rule it belongs to."""
    language = language or detect_language(text)
    return {
        "volunteering_listed_as_employment": find_volunteering_in_experience(text, language),
        "unexplained_gap": find_unexplained_gap(text, language, today),
        "impossible_dates": find_impossible_dates(text, today),
        "first_person_in_cv": find_first_person(text, language),
        "outdated_personal_details": find_outdated_personal_details(text, language),
        "oldest_entry_first": find_oldest_first(text, language),
    }


__all__ = ["ConventionFinding", "DateSpan", "analyze_conventions"]
