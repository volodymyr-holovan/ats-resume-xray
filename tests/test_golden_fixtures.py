"""End-to-end harness: generates each golden fixture, runs the real
pipeline against it, and asserts the triggered rule ids match the golden
expectation exactly. This is the regression net for the whole project —
a change that silently breaks a detector (or makes one over-fire) shows up
here even if no other test happens to cover that exact combination.
"""

import pytest
from golden_expectations import GOLDEN_CASES

from ats_xray.pipeline import analyze_path


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
