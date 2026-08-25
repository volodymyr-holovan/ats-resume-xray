from pathlib import Path

import pytest

import ats_xray.rules  # noqa: F401  (registers the rule set)
from ats_xray.i18n import (
    DEFAULT_LANGUAGE,
    PLURAL_FEW_LANGUAGES,
    RULE_DESCRIPTIONS,
    TRANSLATIONS,
    UI_LANGUAGES,
    rule_description,
    rule_detail,
    rule_fixes,
    sources_path,
    t,
    tn,
)
from ats_xray.rule import all_rules
from ats_xray.score import RATING_THRESHOLDS

REPO_ROOT = Path(__file__).parent.parent


@pytest.mark.parametrize("language", list(UI_LANGUAGES))
def test_every_ui_string_is_translated_into_every_language(language):
    """A half-translated interface shows one language's text inside
    another's page, which reads worse than not offering the language.
    """
    missing = sorted(
        key
        for key, entry in TRANSLATIONS.items()
        if language not in entry and not _optional_for(key, language)
    )

    assert not missing, f"{language} is missing: {missing}"


def _optional_for(key: str, language: str) -> bool:
    """Whether a language is allowed to have no entry for this key.

    Only the 2-4 form: Ukrainian and Russian inflect it differently from
    both 1 and 5+, and no other supported language has anywhere to put it.
    """
    return key.endswith("_few") and language not in PLURAL_FEW_LANGUAGES


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

    assert "1" in filled and "3" in filled and "Skills" in filled
    assert "{" not in filled


@pytest.mark.parametrize("language", list(UI_LANGUAGES))
def test_placeholder_names_match_across_languages(language):
    """A translation that renames or drops a placeholder raises KeyError at
    render time, in that language only -- exactly the kind of bug that
    survives testing in English.
    """
    import string

    for key, entry in TRANSLATIONS.items():
        english = entry.get(DEFAULT_LANGUAGE)
        if english is None:
            # A 2-4 form exists only where a language needs one; the
            # reference spelling lives on the 5+ form of the same stem.
            english = TRANSLATIONS[key.rsplit("_", 1)[0] + "_many"][DEFAULT_LANGUAGE]
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


PLURAL_STEMS = ("cap_reason", "match_missing_must_warning")


@pytest.mark.parametrize("stem", PLURAL_STEMS)
@pytest.mark.parametrize("language", list(UI_LANGUAGES))
def test_every_count_resolves_to_a_real_sentence(stem, language):
    """The resolver falls back rather than raising, so a missing form would
    quietly show the wrong number agreement instead of failing. Walking the
    counts is what catches it."""
    for count in (1, 2, 4, 5, 11, 21, 22, 25, 101):
        rendered = tn(stem, count, language, cap=59, uncapped=88)

        assert rendered.startswith("[") is False, f"{stem}/{language}/{count} unresolved"
        assert str(count) in rendered, f"{stem}/{language}/{count} lost the number"
        assert "{" not in rendered


@pytest.mark.parametrize("stem", PLURAL_STEMS)
def test_slavic_counts_take_three_distinct_forms(stem):
    """1, 3 and 7 decline differently in Ukrainian and Russian. If two of
    them come back identical, a form is missing and the fallback covered
    it."""
    for language in PLURAL_FEW_LANGUAGES:
        one, few, many = (
            tn(stem, count, language, cap=59, uncapped=88).replace(str(count), "N")
            for count in (1, 3, 7)
        )

        assert one != few != many != one, f"{stem}/{language} does not distinguish 1/3/7"


def test_every_token_the_analysis_emits_has_a_translation():
    """The gap this closes: the analysis names things in English lowercase
    -- "email", "experience", "bachelor" -- and those names were being
    interpolated straight into German and Ukrainian sentences. Anything the
    code can put into a translated slot has to be in the vocabulary, and a
    new education level or section added later has to fail here rather
    than reach a reader."""
    from ats_xray.credentials import EDUCATION_RANK, STUDY_FIELDS_BY_LANGUAGE
    from ats_xray.field_report import EXPECTED_SECTIONS
    from ats_xray.i18n import VOCABULARY

    emitted = (
        {"email", "phone", "header", "footer"}
        | set(EXPECTED_SECTIONS)
        | set(EDUCATION_RANK)
        | {field for fields in STUDY_FIELDS_BY_LANGUAGE.values() for field in fields}
    )
    missing = sorted(emitted - set(VOCABULARY))

    assert not missing, f"tokens with no translation: {missing}"


@pytest.mark.parametrize("language", list(UI_LANGUAGES))
def test_no_internal_token_survives_into_a_rendered_sentence(language):
    import re

    from ats_xray.i18n import VOCABULARY, term

    for token in VOCABULARY:
        translated = term(token, language)
        if translated == token:
            continue
        rendered = t("detail_contact_one", language, found=token, missing=token)

        # Whole words only: "phone" lives inside "telefoonnummer" and
        # "telephone" without either being a leak.
        assert not re.search(rf"{re.escape(token)}", rendered), (
            f"{language}: {token} reached the reader untranslated"
        )
        assert translated in rendered


@pytest.mark.parametrize("language", list(UI_LANGUAGES))
def test_every_rule_has_a_readable_name_in_every_language(language):
    """The rule id is what the code calls it -- lowercase, English,
    underscored. It was reaching readers in two places: under each page
    image ("Page 1 — section_missing_under_naive_parsing") and in the score
    breakdown, which told a German reader "Abzüge: docx_table_content
    (-25)". A rule added without a name would put it back."""
    from ats_xray.i18n import RULE_NAMES, rule_name

    missing = sorted(rule.id for rule in all_rules() if rule.id not in RULE_NAMES)
    assert not missing, f"rules with no short name: {missing}"

    untranslated = sorted(
        rule.id for rule in all_rules() if language not in RULE_NAMES[rule.id]
    )
    assert not untranslated, f"{language} is missing rule names: {untranslated}"

    for rule in all_rules():
        name = rule_name(rule.id, language)
        assert name != rule.id, f"{language}/{rule.id} falls back to the id"
        assert "_" not in name, f"{language}/{rule.id} still reads like an identifier"
        assert len(name) <= 40, f"{language}/{rule.id} is too long for a caption: {name!r}"


def test_the_score_breakdown_names_its_rules(language="de"):
    """The deduction list is built before a language is chosen, so it
    carries pairs and is named at render time. If that wiring breaks it
    fails loudly here rather than showing snake_case to a reader."""
    rendered = t(
        "detail_structure_deductions",
        language,
        deductions=(("docx_table_content", 25), ("pdf_textless_image", 10)),
    )

    assert "docx_table_content" not in rendered
    assert "Inhalt in einer Tabelle (-25)" in rendered
    assert "(-10)" in rendered
