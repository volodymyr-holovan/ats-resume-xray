"""Rule model and registry.

Each ``Rule`` is metadata for one documented resume-parsing risk: what it
means, how severe it is, and which entry in ``research_sources.md`` backs
the claim. Rules carry no detection logic — evaluating an actual resume
against the rule set (the "rule engine runner") is a separate concern, so
the documented claims and the code that checks for them can be reviewed
independently.
"""

from dataclasses import dataclass

SEVERITIES = ("high", "medium", "low")
"""Most serious first."""

SEVERITY_ORDER = {severity: rank for rank, severity in enumerate(SEVERITIES)}
"""Sort key for listing findings most serious first. The findings zone, the
command-line report and the action plan all list them that way, and each had
written this mapping out for itself."""

PARSING = "parsing"
CONVENTION = "convention"
_VALID_CATEGORIES = (PARSING, CONVENTION)


@dataclass(frozen=True)
class Rule:
    id: str
    description: str
    severity: str
    source: str
    """Key into research_sources.md, not a raw URL — so a citation can be
    corrected or expanded in one place without touching any Python."""
    category: str = PARSING
    """What kind of problem this is, which decides what it may count against.

    ``parsing``: the file risks being read wrongly by software. These are what
    the parse-readiness score measures.

    ``convention``: the file reads perfectly and says something a recruiter in
    that country does not expect -- volunteering listed as a job in a German
    CV, a date range that ends before it starts. Real problems, reported with
    the rest, and kept out of the score, because a parser has no difficulty
    with any of them and the score has never claimed to measure anything
    else."""

    def __post_init__(self) -> None:
        if self.severity not in SEVERITIES:
            raise ValueError(f"Invalid severity {self.severity!r}, expected one of {SEVERITIES}")
        if self.category not in _VALID_CATEGORIES:
            raise ValueError(f"Invalid category {self.category!r}, expected one of {_VALID_CATEGORIES}")


_REGISTRY: dict[str, Rule] = {}


def register(rule: Rule) -> Rule:
    if rule.id in _REGISTRY:
        raise ValueError(f"Duplicate rule id: {rule.id!r}")
    _REGISTRY[rule.id] = rule
    return rule


def all_rules() -> list[Rule]:
    return list(_REGISTRY.values())


def get_rule(rule_id: str) -> Rule:
    return _REGISTRY[rule_id]
