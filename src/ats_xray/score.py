"""Parse Readiness Score: how much of a resume survives automated reading.

Deliberately **not** called an "ATS score". Public checkers blend two very
different things into one number: whether the file parses, and how well its
wording matches a specific job posting. The second half needs a job
description and a weighting the employer chose, neither of which this tool
has -- which is why the same resume scores 71 on one commercial checker and
55 on another against the same posting. Publishing a number like that
without the inputs behind it is the black box this project exists to avoid.

So this measures only the half that is actually knowable from the file
alone: parse readiness. Every component below is computed from evidence the
tool can show you, and ``ScoreBreakdown`` carries the arithmetic so the UI
can display the full derivation rather than just the total.

Components:

- **Contact reachability** -- can a parser recover an email or phone from
  the *naive* extraction? Scored against the worst case rather than the best,
  because a candidate an employer cannot contact is unreachable regardless of
  how well the rest parsed.
- **Section survival** -- of the sections that genuinely exist in the resume
  (found by layout-aware reading), what share still survives naive reading?
  Sections the candidate simply did not write are excluded from the
  denominator: their absence is a content choice, not a parsing failure.
- **Structural integrity** -- starts at 100 and deducts for each triggered
  structural rule, weighted by that rule's severity.

Wording lives in ``i18n``, not here: components carry a translation key and
its parameters so the same breakdown renders in any supported language.
"""

from dataclasses import dataclass, field

from .engine import Finding

CONTACT_WEIGHT = 30
SECTIONS_WEIGHT = 30
STRUCTURE_WEIGHT = 40

SEVERITY_PENALTY = {"high": 25, "medium": 10, "low": 5}

_FIELD_RULES = {"missing_contact_field", "section_missing_under_naive_parsing"}
"""Rules already reflected in the contact and section components. Excluded
from the structural deduction so one problem is not counted twice."""


@dataclass(frozen=True)
class Component:
    name_key: str
    score: float
    weight: float
    detail_key: str
    detail_params: dict = field(default_factory=dict)


HIGH_SEVERITY_CAPS = {1: 79, 2: 59}
"""A high-severity finding means content is at risk of being dropped or
scrambled outright. Weighted averaging alone can bury that: one such finding
costs only a few points overall, which would let a resume with a table
swallowing its entire skills list still read as "parses cleanly". So the
count of high-severity findings caps the headline number, and the cap is
reported rather than silently applied."""

RATING_THRESHOLDS = ((85, "rating_clean"), (65, "rating_mostly"), (40, "rating_significant"))


@dataclass(frozen=True)
class ScoreBreakdown:
    total: int
    components: list[Component] = field(default_factory=list)
    uncapped_total: int = 0
    cap_key: str | None = None
    cap_params: dict = field(default_factory=dict)

    @property
    def rating_key(self) -> str:
        # "Parses poorly" would be the wrong thing to say about a document
        # that is not a CV: it parsed fine, it just is not one.
        if self.cap_key == "cap_reason_not_a_resume":
            return "rating_not_a_resume"
        for threshold, key in RATING_THRESHOLDS:
            if self.total >= threshold:
                return key
        return "rating_poor"


NOT_A_RESUME_SCORE = 0
"""What a document scores when nothing in it says "CV".

Reported after someone uploaded a blank character sheet and got a
respectable number back. The structure component was the cause: a document
with no columns, no tables and no images triggers no rules, so it scored
full marks for being cleanly parseable -- which was true and useless. A form
with nothing on it parses perfectly and is not a CV.

Zero rather than a low score, with an explanation, because the honest answer
to "how readable is this CV" for something that is not a CV is not a number."""


def looks_like_a_resume(aware_fields: dict) -> bool:
    """Whether the document has anything that marks it as a CV at all.

    The bar is deliberately low -- one contact detail or one recognised
    section heading -- because a real CV in an unusual shape must still get
    through. What it stops is the document that has neither: no email, no
    phone, and nothing the section recogniser knows in any of seven
    languages.
    """
    has_contact = aware_fields["email"]["found"] or aware_fields["phone"]["found"]
    has_section = any(field["found"] for field in aware_fields["sections"].values())
    return has_contact or has_section


def score_resume(aware_fields: dict, naive_fields: dict, findings: list[Finding]) -> ScoreBreakdown:
    """Compute the parse readiness score and the components behind it."""
    if not looks_like_a_resume(aware_fields):
        components = [
            _contact_component(naive_fields),
            _sections_component(aware_fields, naive_fields),
            _structure_component(findings),
        ]
        return ScoreBreakdown(
            total=NOT_A_RESUME_SCORE,
            components=components,
            uncapped_total=NOT_A_RESUME_SCORE,
            cap_key="cap_reason_not_a_resume",
            cap_params={},
        )

    components = [
        _contact_component(naive_fields),
        _sections_component(aware_fields, naive_fields),
        _structure_component(findings),
    ]
    present = [c for c in components if c.weight > 0]

    total_weight = sum(c.weight for c in present)
    weighted = sum(c.score * c.weight for c in present) / total_weight if total_weight else 100.0
    uncapped = round(weighted)

    high_count = sum(1 for f in findings if f.severity == "high")
    cap = HIGH_SEVERITY_CAPS.get(min(high_count, 2)) if high_count else None

    if cap is not None and uncapped > cap:
        return ScoreBreakdown(
            total=cap,
            components=components,
            uncapped_total=uncapped,
            # Separate keys rather than an English plural rule: languages
            # here pluralise differently and some need three forms.
            cap_key="cap_reason_one" if high_count == 1 else "cap_reason_many",
            cap_params={"cap": cap, "count": high_count, "uncapped": uncapped},
        )

    return ScoreBreakdown(total=uncapped, components=components, uncapped_total=uncapped)


def _contact_component(naive_fields: dict) -> Component:
    found = [name for name in ("email", "phone") if naive_fields[name]["found"]]

    if len(found) == 2:
        detail_key, params = "detail_contact_both", {}
    elif found:
        detail_key = "detail_contact_one"
        params = {"found": found[0], "missing": "phone" if found == ["email"] else "email"}
    else:
        detail_key, params = "detail_contact_none", {}

    return Component(
        name_key="component_contact",
        score=len(found) / 2 * 100,
        weight=CONTACT_WEIGHT,
        detail_key=detail_key,
        detail_params=params,
    )


def _sections_component(aware_fields: dict, naive_fields: dict) -> Component:
    present = [s for s, f in aware_fields["sections"].items() if f["found"]]

    if not present:
        return Component(
            name_key="component_sections",
            score=0.0,
            weight=0,
            detail_key="detail_sections_absent",
        )

    survived = [s for s in present if naive_fields["sections"][s]["found"]]
    lost = sorted(s for s in present if s not in survived)

    return Component(
        name_key="component_sections",
        score=len(survived) / len(present) * 100,
        weight=SECTIONS_WEIGHT,
        detail_key="detail_sections_lost" if lost else "detail_sections_all",
        detail_params={
            "survived": len(survived),
            "total": len(present),
            "lost": ", ".join(lost),
        },
    )


def _structure_component(findings: list[Finding]) -> Component:
    structural = [f for f in findings if f.rule.id not in _FIELD_RULES]
    penalty = sum(SEVERITY_PENALTY[f.severity] for f in structural)

    deductions = ", ".join(f"{f.rule.id} (-{SEVERITY_PENALTY[f.severity]})" for f in structural)

    return Component(
        name_key="component_structure",
        score=max(0.0, 100.0 - penalty),
        weight=STRUCTURE_WEIGHT,
        detail_key="detail_structure_deductions" if structural else "detail_structure_clean",
        detail_params={"deductions": deductions},
    )
