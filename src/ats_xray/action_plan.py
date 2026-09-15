"""One ordered list of what to change, gathered from everything else.

The report already says what is wrong three times over: a finding names the
fault, its fix list gives the steps, and the match columns say what the
advert wanted and did not get. All of that is true and none of it is a
plan — the reader still has to decide what to do first, from three lists
that do not know about each other.

This merges them into a single sequence, ordered by what it costs to leave
undone:

1. Anything that risks the file being read wrongly. A skill the parser
   cannot see is worth nothing however well it matches, so structure comes
   before content, and the most serious findings come first.
2. What the CV says against the conventions of where it is going -- the
   volunteering listed as a job, the gap nobody explained. The file reads
   fine; a recruiter reading it does not.
3. What the advert asked for and did not find, largest gain first — which
   is not the order the gaps column happens to be in, because a blocking
   requirement is worth three times a preferred one.
4. Skills that matched but only in an entry that ended years ago.

The steps carry keys rather than sentences. Wording lives in ``i18n``, the
same as everywhere else, so the plan renders in whichever language the
reader has chosen and this module stays free of it.
"""

from dataclasses import dataclass, field

from .rule import PARSING

SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}

REDUNDANT_WITH = {"contact_only_as_link": "missing_contact_field"}
"""Rules whose plan line is the same instruction as another's.

Two findings can be separate diagnoses and one remedy. A CV reachable only
through a LinkedIn link has no email in its text either, so both rules fire
and both say "write your address out in the first three lines" -- true
twice, and in a numbered list it reads as two jobs rather than one.

Only the plan collapses them. In the findings zone both stay, because there
the reader is being told what is wrong rather than what to do, and the two
faults really are different."""


@dataclass(frozen=True)
class Step:
    """One instruction, in the form the renderer needs to write it out.

    ``kind`` says where the sentence comes from:

    * ``"fix"`` -- take this rule's plan line, which states the outcome
      without naming an application. The fix list under the finding is the
      other half of the same advice and stays there: it walks a menu, which
      helps someone sitting in that one editor and nobody else.
    * ``"add"`` / ``"refresh"`` -- a sentence of its own, with parameters.
    """

    kind: str
    rule_id: str = ""
    key: str = ""
    params: dict = field(default_factory=dict)


def build_plan(findings, report=None) -> list[Step]:
    """Every change worth making, most costly omission first.

    ``report`` is a :class:`~ats_xray.match.MatchReport` or None: without a
    pasted advert there is nothing to say about content, and the plan is
    the structural half alone.
    """
    steps: list[Step] = []

    triggered = {finding.rule.id for finding in findings}
    # Parsing before convention, then severity within each: a medium
    # convention finding must not jump a low one that loses content,
    # because the second is what decides whether anything is read at all.
    ordered = sorted(
        findings,
        key=lambda f: (f.rule.category != PARSING, SEVERITY_ORDER[f.severity]),
    )
    for finding in ordered:
        if REDUNDANT_WITH.get(finding.rule.id) in triggered:
            continue
        steps.append(Step(kind="fix", rule_id=finding.rule.id))

    if report is None:
        return steps

    for outcome, points in report.gains:
        steps.append(
            Step(
                kind="add",
                key="plan_add",
                params={"item": outcome.requirement.label, "points": points},
            )
        )

    for outcome in report.stale:
        steps.append(
            Step(
                kind="refresh",
                key="plan_refresh",
                params={"item": outcome.requirement.label, "years": outcome.stale_years},
            )
        )

    return steps
