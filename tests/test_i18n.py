from pathlib import Path

import pytest

import ats_xray.rules  # noqa: F401  (registers the rule set)
from ats_xray.i18n import (
    DEFAULT_LANGUAGE,
    RULE_DESCRIPTIONS,
    TRANSLATIONS,
    UI_LANGUAGES,
    rule_description,
    rule_detail,
    rule_fixes,
    sources_path,
    t,
)
from ats_xray.rule import all_rules
from ats_xray.score import RATING_THRESHOLDS

REPO_ROOT = Path(__file__).parent.parent


@pytest.mark.parametrize("language", list(UI_LANGUAGES))
def test_every_ui_string_is_translated_into_every_language(language):
    """A half-translated interface shows one language's text inside
    another's page, which reads worse than not offering the language.
    """
    missing = sorted(key for key, entry in TRANSLATIONS.items() if language not in entry)

    assert not missing, f"{language} is missing: {missing}"


@pytest.mark.parametrize("language", list(UI_LANGUAGES))
def test_every_rule_description_is_translated_into_every_language(language):
    missing = sorted(rule_id for rule_id, entry in RULE_DESCRIPTIONS.items() if language not in entry)

    assert not missing, f"{language} is missing rule descriptions: {missing}"


def test_every_registered_rule_has_a_description_entry():
    """A rule added without a translation entry would fall back to English
    for everyone; this makes that a failing test rather than a silent gap.
    """
    missing = sorted(rule.id for rule in all_rules() if rule.id not in RULE_DESCRIPTIONS)

    assert not missing, f"rules with no translation entry: {missing}"


def test_every_rating_key_is_translated():
    """Rating keys are produced by score.py, so a renamed threshold would
    otherwise surface as a bracketed placeholder in the score box.
    """
    keys = [key for _, key in RATING_THRESHOLDS] + ["rating_poor"]

    for key in keys:
        assert key in TRANSLATIONS, f"{key} has no translation entry"


def test_unknown_key_is_visible_rather_than_fatal():
    assert t("no_such_key", "en") == "[no_such_key]"


def test_unknown_language_falls_back_to_english():
    assert t("findings_heading", "xx") == TRANSLATIONS["findings_heading"][DEFAULT_LANGUAGE]


def test_placeholders_are_filled():
    filled = t("detail_sections_lost", "en", survived=1, total=3, lost="skills")

    assert "1" in filled and "3" in filled and "skills" in filled
    assert "{" not in filled


@pytest.mark.parametrize("language", list(UI_LANGUAGES))
def test_placeholder_names_match_across_languages(language):
    """A translation that renames or drops a placeholder raises KeyError at
    render time, in that language only -- exactly the kind of bug that
    survives testing in English.
    """
    import string

    for key, entry in TRANSLATIONS.items():
        english = entry[DEFAULT_LANGUAGE]
        translated = entry.get(language)
        if translated is None:
            continue
        expected = {f for _, f, _, _ in string.Formatter().parse(english) if f}
        actual = {f for _, f, _, _ in string.Formatter().parse(translated) if f}
        assert actual == expected, f"{language}/{key}: placeholders {actual} != {expected}"


def test_rule_description_falls_back_to_the_rule_text():
    fallback = "some new rule not yet translated"

    assert rule_description("rule_that_does_not_exist", "uk", fallback) == fallback


@pytest.mark.parametrize("language", list(UI_LANGUAGES))
def test_every_rule_has_a_detail_and_fixes_in_every_language(language):
    """A finding a reader can expand but that then explains nothing is
    worse than one that never offered to explain: the expander promises
    depth. Every rule owes both halves in every language it advertises."""
    no_detail = sorted(rule.id for rule in all_rules() if not rule_detail(rule.id, language))
    no_fixes = sorted(rule.id for rule in all_rules() if not rule_fixes(rule.id, language))

    assert not no_detail, f"{language} rules with no detail: {no_detail}"
    assert not no_fixes, f"{language} rules with no fixes: {no_fixes}"


@pytest.mark.parametrize("language", list(UI_LANGUAGES))
def test_fixes_are_actual_steps_not_one_liners(language):
    """The point of the fix list is choice: the direct change, an
    alternative when it is not available, and a way to confirm it worked.
    A single vague line would satisfy the test above and help nobody."""
    for rule in all_rules():
        fixes = rule_fixes(rule.id, language)

        assert len(fixes) >= 2, f"{rule.id} ({language}) offers only {len(fixes)} fix"
        assert all(len(fix) > 30 for fix in fixes), f"{rule.id} ({language}) has a stub fix"


@pytest.mark.parametrize("language", list(UI_LANGUAGES))
def test_sources_file_exists_for_every_language(language):
    """The findings link straight into this file, so a language whose
    translation was never written would send readers to a 404."""
    path = REPO_ROOT / sources_path(language)

    assert path.is_file(), f"{language} points at a missing file: {path}"


@pytest.mark.parametrize("language", list(UI_LANGUAGES))
def test_every_cited_source_anchor_resolves_in_every_language(language):
    """Rules cite an anchor, not a document. Translating the prose but
    renaming a heading would break the deep link silently."""
    text = (REPO_ROOT / sources_path(language)).read_text(encoding="utf-8")
    missing = sorted({rule.source for rule in all_rules() if f"## {rule.source}" not in text})

    assert not missing, f"{language} sources file is missing anchors: {missing}"


def test_unknown_language_falls_back_to_the_english_sources_file():
    assert sources_path("kl") == sources_path(DEFAULT_LANGUAGE)


@pytest.mark.parametrize("severity", ["high", "medium", "low"])
def test_every_severity_has_a_translated_label(severity):
    """The badge on each finding is the reader's only cue that severities
    differ at all, so an untranslated one leaks English into every page."""
    for language in UI_LANGUAGES:
        label = t(f"severity_{severity}", language)

        assert label and label.strip() == label
