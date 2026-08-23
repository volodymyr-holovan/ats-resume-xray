import pytest

import ats_xray.rules  # noqa: F401  (registers the rule set)
from ats_xray.i18n import (
    DEFAULT_LANGUAGE,
    RULE_DESCRIPTIONS,
    TRANSLATIONS,
    UI_LANGUAGES,
    rule_description,
    t,
)
from ats_xray.rule import all_rules
from ats_xray.score import RATING_THRESHOLDS


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
