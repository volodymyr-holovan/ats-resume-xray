"""Compare a parsed vacancy against a parsed CV.

Two things make this different from a keyword counter.

The first is that requirements compare by their own rules. A Master's degree
satisfies an advert asking for a Bachelor. Five years of experience satisfies
a request for three. C1 German satisfies B2. Only skills are all-or-nothing,
and even they get partial credit when the advert said the requirement was
optional.

The second is that a match is only worth anything if the parser can see it.
This tool already knows which parts of a CV survive a layout-blind read, so
a skill that matches only in the layout-aware text is reported as a match at
risk: the human reader would find it, the software filtering the pile might
not. That is the one thing a generic keyword matcher cannot tell you.
"""

from dataclasses import dataclass, field
from datetime import date
from functools import cached_property

from .credentials import (
    CEFR_RANK,
    EDUCATION_RANK,
    LanguageFact,
    find_education,
    find_experience_months,
    find_languages,
    find_licence,
)
from .langid import detect_language
from .normalize import contains_phrase, fold, tokens
from .recency import find_dated_entries, is_stale, last_used, skills_listed, years_since
from .sections import split_into_sections
from .skills_lexicon import SKILLS_BY_ID, find_skills, label_for
from .terms import WEIGHT_INTRODUCED, WEIGHT_NOUN, WEIGHT_TASK
from .vacancy import Requirement

MUST_WEIGHT = 3
NICE_WEIGHT = 1
"""A must-have counts for three preferences. The exact ratio is a judgement
call; what matters is that missing one blocking requirement outweighs
collecting several optional ones."""

PARTIAL_CREDIT = 0.5

GUESS_CONFIDENCE = {WEIGHT_INTRODUCED: 1.0, WEIGHT_NOUN: 0.75, WEIGHT_TASK: 0.5}
"""How far a keyword the gazetteer does not know is trusted, by how the
advert evidenced it.

A named skill is a fact about the advert; a guessed keyword is a reading of
it, and the readings are not equally sure. "Kenntnisse in X" says X is
wanted. A capitalised noun in a German bullet only suggests it. A word taken
out of a duties line is the weakest of the three -- the block describes work
rather than stating requirements.

Scoring all three like a named skill let one guess cost a candidate as much
as the degree the advert asked for. They still count, at what they are
worth."""

RATING_THRESHOLDS = (
    (80, "match_rating_strong"),
    (60, "match_rating_good"),
    (40, "match_rating_partial"),
    (0, "match_rating_weak"),
)

EXPERIENCE_PARTIAL_RATIO = 0.7
"""Someone with two years against a three-year requirement is not a
mismatch, and adverts routinely ask for more than the job needs."""

MAX_EXTRAS = 12

MAX_GAINS = 3
"""How many improvements to name.

A list of everything missing is the gaps column, which is already on
screen. This answers a different question -- what should I do first --
and an answer with ten items in it is not an answer."""


@dataclass(frozen=True)
class Outcome:
    requirement: Requirement
    status: str
    evidence: str = ""
    at_risk: bool = False
    stale: bool = False
    stale_years: int = 0
    """How long ago the newest dated use ended, when ``stale``.

    Carried on the outcome rather than only inside note_params, because
    which note wins is a presentation decision: a skill that is both
    invisible to the parser and years old shows the at-risk sentence, whose
    parameters have no years in them. The action plan read the years from
    there and told the reader a skill last used six years ago had ended
    "0 years ago"."""
    note_key: str | None = None
    note_params: dict = field(default_factory=dict)

    @property
    def weight(self) -> float:
        base = MUST_WEIGHT if self.requirement.must else NICE_WEIGHT
        # Only a guessed keyword carries an evidence weight; everything else
        # is a requirement the advert named, and counts in full.
        return base * GUESS_CONFIDENCE.get(self.requirement.detail.get("weight"), 1.0)

    @property
    def credit(self) -> float:
        return {"met": 1.0, "partial": PARTIAL_CREDIT}.get(self.status, 0.0)


@dataclass(frozen=True)
class MatchReport:
    outcomes: tuple[Outcome, ...]
    score: int
    rating_key: str
    extras: tuple[str, ...]
    missing_must: tuple[Outcome, ...]
    at_risk: tuple[Outcome, ...]
    stale: tuple[Outcome, ...] = ()
    gains: tuple[tuple[Outcome, int], ...] = ()
    """What each unmet requirement would add to the score, best first."""

    def of_status(self, status: str) -> list[Outcome]:
        return [o for o in self.outcomes if o.status == status]


class _Cv:
    """What the matcher knows about one CV, each fact worked out once.

    Every requirement in an advert is compared against the same CV, and each
    comparison used to work out again whatever it needed: which line mentions a
    skill (by running the lexicon over the CV line by line, per skill), which
    skills the Skills section lists (per skill), which languages the CV states
    (per language asked for), the CV's words for a keyword the reader typed
    (per keyword). Here each is read on first use and kept for the rest of the
    match, and the evaluators take the CV instead of eight arguments about it.

    For scale: a real CV against one advert went from 169 lexicon scans to 86,
    and from about 52 ms to 43. The fixed costs -- detecting the language,
    reading the whole CV for skills, finding its dated entries -- are most of
    what is left, and each is paid once.

    Lives for one evaluate_match call and no longer.
    """

    def __init__(self, aware_text: str, naive_text: str, today: date | None):
        self.text = aware_text
        self.today = today
        # The CV has its own language, which need not be the advert's: a
        # German CV is sometimes measured against an English posting.
        self.language = detect_language(aware_text)
        self.sections = split_into_sections(aware_text)
        self.skills = set(find_skills(aware_text, self.language))
        self.naive_skills = set(find_skills(naive_text, self.language)) if naive_text else self.skills
        # The dated blocks of the CV, so a matched skill can be told apart into
        # one the candidate still uses and one they last touched a decade ago.
        self.entries = find_dated_entries(aware_text, today)

        self._evidence: dict[str, str] = {}
        self._lines_read = 0

    @cached_property
    def lines(self) -> list[str]:
        return [line.strip() for line in self.text.splitlines() if line.strip()]

    def evidence_for(self, skill_id: str) -> str:
        """The first line mentioning a skill, as the reader's evidence.

        Reads down the CV only as far as the skill asked about, and never
        reads a line twice in one match: every skill the line holds is noted
        on the way past, so the next skill asked for is often already known.
        Reading every line up front cost more than it saved -- most adverts
        match a handful of skills, most of them near the top."""
        while skill_id not in self._evidence and self._lines_read < len(self.lines):
            line = self.lines[self._lines_read]
            self._lines_read += 1
            for found in find_skills(line, self.language):
                self._evidence.setdefault(found, line[:160])
        return self._evidence.get(skill_id, "")

    @cached_property
    def listed_skills(self) -> frozenset[str]:
        return skills_listed(self.text, self.language)

    @cached_property
    def words(self) -> list[str]:
        return tokens(self.text)

    @cached_property
    def line_words(self) -> list[tuple[str, list[str]]]:
        return [(line, tokens(line)) for line in self.lines]

    @cached_property
    def languages(self) -> dict[str, LanguageFact]:
        scope = "\n".join(part for part in (self.sections.get("languages"), self.text) if part)
        return {fact.language: fact for fact in find_languages(scope, self.language)}


def evaluate_match(
    requirements: list[Requirement],
    aware_text: str,
    naive_text: str = "",
    today: date | None = None,
) -> MatchReport:
    cv = _Cv(aware_text, naive_text, today)
    outcomes = [_evaluate(requirement, cv) for requirement in requirements]

    total_weight = sum(o.weight for o in outcomes)
    earned = sum(o.weight * o.credit for o in outcomes)
    score = round(earned / total_weight * 100) if total_weight else 0

    required_ids = {r.key for r in requirements if r.kind == "skill"}
    extras = tuple(sorted(cv.skills - required_ids))[:MAX_EXTRAS]

    return MatchReport(
        outcomes=tuple(outcomes),
        score=score,
        rating_key=next(key for threshold, key in RATING_THRESHOLDS if score >= threshold),
        extras=extras,
        missing_must=tuple(o for o in outcomes if o.status == "missing" and o.requirement.must),
        at_risk=tuple(o for o in outcomes if o.at_risk),
        stale=tuple(o for o in outcomes if o.stale),
        gains=_gains(outcomes, total_weight),
    )


def _gains(outcomes: list[Outcome], total_weight: int) -> tuple[tuple[Outcome, int], ...]:
    """The unmet requirements ranked by what each would add to the score.

    The gaps column says what is missing. This says which of them to do
    first, which is not the same list: a required item nobody would guess
    matters three times what an optional one does, and two items with the
    same label can be worth very different numbers.

    Computed rather than estimated -- the score is a weighted average, so
    the gain from meeting one requirement is exactly its remaining share.
    """
    if not total_weight:
        return ()
    ranked = sorted(
        (
            (outcome, round((1 - outcome.credit) * outcome.weight / total_weight * 100))
            for outcome in outcomes
            if outcome.credit < 1
        ),
        key=lambda pair: (-pair[1], pair[0].requirement.label),
    )
    return tuple(pair for pair in ranked if pair[1] > 0)[:MAX_GAINS]


def _evaluate(requirement: Requirement, cv: _Cv) -> Outcome:
    if requirement.kind == "skill":
        return _evaluate_skill(requirement, cv)
    if requirement.kind == "experience":
        return _evaluate_experience(requirement, cv)
    if requirement.kind == "education":
        return _evaluate_education(requirement, cv)
    if requirement.kind == "language":
        return _evaluate_language(requirement, cv)
    if requirement.kind == "licence":
        return _evaluate_licence(requirement, cv)
    return Outcome(requirement, "missing")


def _evaluate_skill(requirement: Requirement, cv: _Cv) -> Outcome:
    if requirement.key not in SKILLS_BY_ID:
        return _evaluate_custom_keyword(requirement, cv)

    if requirement.key not in cv.skills:
        return Outcome(requirement, "missing")

    at_risk = requirement.key not in cv.naive_skills
    stale = is_stale(
        requirement.key, cv.text, cv.entries, cv.today, cv.language, listed_skills=cv.listed_skills
    )
    stale_years = (
        years_since(last_used(requirement.key, cv.entries, cv.language), cv.today)
        if stale
        else 0
    )

    # A skill the parser cannot see outranks one the employer might ask
    # about: the first loses the match outright, the second only invites a
    # question. Both are true; only one fits on the line.
    if at_risk:
        note_key = "match_note_skill_at_risk"
        note_params = {"skill": label_for(requirement.key)}
    elif stale:
        note_key = "match_note_skill_stale"
        note_params = {"skill": label_for(requirement.key), "years": stale_years}
    else:
        note_key, note_params = None, {}

    return Outcome(
        requirement,
        "met",
        evidence=cv.evidence_for(requirement.key),
        at_risk=at_risk,
        stale=stale,
        stale_years=stale_years,
        note_key=note_key,
        note_params=note_params,
    )


def _evaluate_custom_keyword(requirement: Requirement, cv: _Cv) -> Outcome:
    """A keyword the reader typed in, which by definition is not in the
    lexicon. Compared as a phrase against the CV, with the same tolerance
    for inflection the lexicon gets."""
    phrase = fold(requirement.label)
    if not phrase or not contains_phrase(cv.words, phrase):
        return Outcome(requirement, "missing")
    evidence = next((line[:160] for line, words in cv.line_words if contains_phrase(words, phrase)), "")
    return Outcome(requirement, "met", evidence=evidence)


def _evaluate_experience(requirement: Requirement, cv: _Cv) -> Outcome:
    # Dates outside the experience section belong to studies and courses;
    # counting those as professional experience would inflate every CV.
    scope = cv.sections.get("experience") or cv.text
    months = find_experience_months(scope, today=cv.today)
    required_months = requirement.detail.get("years", 0) * 12
    years_have = round(months / 12, 1)
    params = {"have": years_have, "want": requirement.detail.get("years", 0)}

    if months >= required_months:
        status = "met"
    elif required_months and months >= required_months * EXPERIENCE_PARTIAL_RATIO:
        status = "partial"
    else:
        status = "missing"

    return Outcome(
        requirement,
        status,
        evidence=f"{years_have}",
        note_key="match_note_experience",
        note_params=params,
    )


def _evaluate_education(requirement: Requirement, cv: _Cv) -> Outcome:
    scope = cv.sections.get("education") or cv.text
    fact = find_education(scope, cv.language)
    wanted_rank = EDUCATION_RANK.get(requirement.key, 0)
    equivalent = requirement.detail.get("equivalent_accepted", False)

    if fact is None:
        # "oder vergleichbare Qualifikation" means the degree is not a gate,
        # so its absence is a soft gap rather than a disqualification.
        return Outcome(
            requirement,
            "partial" if equivalent else "missing",
            note_key="match_note_education_missing",
            note_params={"want": requirement.label},
        )

    params = {"have": fact.level, "want": requirement.key}

    if fact.rank >= wanted_rank:
        wanted_field = requirement.detail.get("field")
        if wanted_field and fact.field and fact.field != wanted_field:
            return Outcome(
                requirement,
                "partial",
                evidence=fact.evidence,
                note_key="match_note_education_field",
                note_params={"have": fact.field or "-", "want": wanted_field},
            )
        return Outcome(requirement, "met", evidence=fact.evidence, note_key="match_note_education_ok", note_params=params)

    return Outcome(
        requirement,
        "partial" if equivalent else "missing",
        evidence=fact.evidence,
        note_key="match_note_education_lower",
        note_params=params,
    )


def _evaluate_language(requirement: Requirement, cv: _Cv) -> Outcome:
    wanted = requirement.detail.get("level")
    have = cv.languages.get(requirement.key)

    if have is None:
        return Outcome(
            requirement,
            "missing",
            note_key="match_note_language_missing",
            note_params={"lang": requirement.key.upper()},
        )
    if wanted is None:
        return Outcome(requirement, "met", evidence=have.level.upper())

    gap = CEFR_RANK.get(wanted, 0) - have.rank
    status = "met" if gap <= 0 else "partial" if gap == 1 else "missing"
    return Outcome(
        requirement,
        status,
        evidence=have.level.upper(),
        note_key="match_note_language",
        note_params={
            "lang": requirement.key.upper(),
            "have": have.level.upper(),
            "want": wanted.upper(),
        },
    )


def _evaluate_licence(requirement: Requirement, cv: _Cv) -> Outcome:
    found = find_licence(cv.text)
    if found is None:
        return Outcome(requirement, "missing", note_key="match_note_licence_missing", note_params={})
    return Outcome(requirement, "met", evidence=found)
