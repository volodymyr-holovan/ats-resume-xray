"""End-to-end harness: generates each golden fixture, runs the real
pipeline against it, and asserts the triggered rule ids match the golden
expectation exactly. This is the regression net for the whole project —
a change that silently breaks a detector (or makes one over-fire) shows up
here even if no other test happens to cover that exact combination.
"""

import pytest
from golden_expectations import GOLDEN_CASES

from ats_xray.pipeline import analyze_path
from ats_xray.rule import PARSING, all_rules


@pytest.mark.parametrize(
    "generator,suffix,expected_rule_ids",
    GOLDEN_CASES,
    ids=[case[0].__name__ for case in GOLDEN_CASES],
)
def test_golden_fixture_triggers_expected_rules_exactly(generator, suffix, expected_rule_ids, tmp_path):
    fixture_path = tmp_path / f"{generator.__name__}{suffix}"

    generator(fixture_path)
    result = analyze_path(str(fixture_path))

    actual_rule_ids = {finding.rule.id for finding in result.findings}
    assert actual_rule_ids == expected_rule_ids


def test_every_parsing_rule_has_a_fixture_that_fires_it():
    """CONTRIBUTING asks for a fixture with every new rule. This is what
    makes that an actual requirement rather than a request.

    Three rules had drifted out of the set by the time anyone counted, and
    one of them -- the unembedded font -- had gone without for a reason
    worth knowing: no library here can write such a file, so the generator
    had to assemble the PDF by hand. A promise nothing enforces is how that
    happens quietly.

    Convention rules are deliberately not covered here. They never reach the
    rule engine's findings and are tested against text in test_conventions.
    """
    covered = set().union(*(ids for _, _, ids in GOLDEN_CASES))
    parsing = {rule.id for rule in all_rules() if rule.category == PARSING}

    assert not parsing - covered, f"no golden fixture fires {sorted(parsing - covered)}"
