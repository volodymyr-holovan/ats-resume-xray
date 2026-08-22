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
    name: str
    score: float
    weight: float
    detail: str


HIGH_SEVERITY_CAPS = {1: 79, 2: 59}
"""A high-severity finding means content is at risk of being dropped or
scrambled outright. Weighted averaging alone can bury that: one such finding
costs only a few points overall, which would let a resume with a table
swallowing its entire skills list still read as "parses cleanly". So the
count of high-severity findings caps the headline number, and the cap is
reported rather than silently applied."""


@dataclass(frozen=True)
class ScoreBreakdown:
    total: int
    components: list[Component] = field(default_factory=list)
    uncapped_total: int = 0
    cap_reason: str | None = None

    @property
    def rating(self) -> str:
        if self.total >= 85:
            return "Parses cleanly"
        if self.total >= 65:
            return "Mostly parses, some risk"
        if self.total >= 40:
            return "Significant parsing risk"
        return "Likely to parse badly"


def score_resume(aware_fields: dict, naive_fields: dict, findings: list[Finding]) -> ScoreBreakdown:
    """Compute the parse readiness score and the components behind it."""
    components = [
        _contact_component(naive_fields),
        _sections_component(aware_fields, naive_fields),
        _structure_component(findings),
    ]
    present = [c for c in components if c.weight > 0]

    total_weight = sum(c.weight for c in present)
    weighted = sum(c.score * c.weight for c in present) / total_weight if total_weight else 100.0
    uncapped = round(weighted)

    high_count = sum(1 for f in findings if f.rule.severity == "high")
    cap = HIGH_SEVERITY_CAPS.get(min(high_count, 2)) if high_count else None

    if cap is not None and uncapped > cap:
        plural = "finding" if high_count == 1 else "findings"
        return ScoreBreakdown(
            total=cap,
            components=components,
            uncapped_total=uncapped,
            cap_reason=f"Capped at {cap}: {high_count} high-severity {plural} put content at risk of being lost",
        )

    return ScoreBreakdown(total=uncapped, components=components, uncapped_total=uncapped)


def _contact_component(naive_fields: dict) -> Component:
    found = [name for name in ("email", "phone") if naive_fields[name]["found"]]

    if len(found) == 2:
        detail = "Email and phone both recovered from a plain, layout-blind read"
    elif found:
        missing = "phone" if found == ["email"] else "email"
        detail = f"{found[0].capitalize()} recovered, but no {missing} found"
    else:
        detail = "Neither email nor phone could be recovered"

    return Component(
        name="Contact reachability",
        score=len(found) / 2 * 100,
        weight=CONTACT_WEIGHT,
        detail=detail,
    )


def _sections_component(aware_fields: dict, naive_fields: dict) -> Component:
    present = [s for s, f in aware_fields["sections"].items() if f["found"]]

    if not present:
        return Component(
            name="Section survival",
            score=0.0,
            weight=0,
            detail="No standard section headings found at all, so there is nothing to compare",
        )

    survived = [s for s in present if naive_fields["sections"][s]["found"]]
    lost = [s for s in present if s not in survived]

    detail = f"{len(survived)} of {len(present)} sections survive a layout-blind read"
    if lost:
        detail += f" (lost: {', '.join(sorted(lost))})"

    return Component(
        name="Section survival",
        score=len(survived) / len(present) * 100,
        weight=SECTIONS_WEIGHT,
        detail=detail,
    )


def _structure_component(findings: list[Finding]) -> Component:
    structural = [f for f in findings if f.rule.id not in _FIELD_RULES]
    penalty = sum(SEVERITY_PENALTY[f.rule.severity] for f in structural)

    if not structural:
        detail = "No structural parsing risks detected"
    else:
        parts = [f"{f.rule.id} (-{SEVERITY_PENALTY[f.rule.severity]})" for f in structural]
        detail = "Deductions: " + ", ".join(parts)

    return Component(
        name="Structural integrity",
        score=max(0.0, 100.0 - penalty),
        weight=STRUCTURE_WEIGHT,
        detail=detail,
    )
