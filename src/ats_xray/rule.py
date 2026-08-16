"""Rule model and registry.

Each ``Rule`` is metadata for one documented resume-parsing risk: what it
means, how severe it is, and which entry in ``research_sources.md`` backs
the claim. Rules carry no detection logic — evaluating an actual resume
against the rule set (the "rule engine runner") is a separate concern, so
the documented claims and the code that checks for them can be reviewed
independently.
"""

from dataclasses import dataclass

_VALID_SEVERITIES = ("high", "medium", "low")


@dataclass(frozen=True)
class Rule:
    id: str
    description: str
    severity: str
    source: str
    """Key into research_sources.md, not a raw URL — so a citation can be
    corrected or expanded in one place without touching any Python."""

    def __post_init__(self) -> None:
        if self.severity not in _VALID_SEVERITIES:
            raise ValueError(f"Invalid severity {self.severity!r}, expected one of {_VALID_SEVERITIES}")


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
