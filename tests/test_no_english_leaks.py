"""Nothing the analysis names in English may reach a reader in another language.

The findings and the score carry evidence as data -- which section was lost,
which contact detail was missing, which zone a repeated line sat in -- and
those values are the names the code uses: lowercase English identifiers.
``i18n.VOCABULARY`` translates them on the way to the screen, and
``TRANSLATED_PARAMS`` says which placeholders hold one.

The two halves can drift, and did: the placeholder was named ``sections``
and the frozenset said ``section``, so the single most common finding
printed "Abschnitte experience, skills" in German for as long as the
mechanism existed. Every unit test passed the whole time, because each one
checked a key it named itself.

So this walks the real pipeline instead. A file goes in, every finding and
every score component comes out rendered in all seven languages, and a bare
identifier anywhere in that text fails.
"""

import re

import pytest

import ats_xray.rules  # noqa: F401  (registers the rule set)
from ats_xray.i18n import UI_LANGUAGES, VOCABULARY, rule_detail, t, term, tn
from ats_xray.pipeline import analyze_bytes

from golden_generators import two_column_pdf

NON_ENGLISH = [language for language in UI_LANGUAGES if language != "en"]


@pytest.fixture(scope="module")
def analysed(tmp_path_factory):
    """A CV whose sections survive layout-aware reading and vanish without
    it -- the shape that produces both a finding with section names in it
    and a score with a component detail listing them."""
    path = tmp_path_factory.mktemp("leaks") / "two-column.pdf"
    two_column_pdf(str(path))
    return analyze_bytes(path.read_bytes(), path.name)


def _rendered(result, language):
    """Everything this analysis would put in front of a reader."""
    for finding in result.findings:
        yield finding.rule.id, t(finding.evidence_key, language, **finding.evidence_params)
        yield finding.rule.id, rule_detail(finding.rule.id, language)
    for component in result.score.components:
        yield component.name_key, t(component.name_key, language)
        yield component.detail_key, t(component.detail_key, language, **component.detail_params)
    if result.score.cap_key:
        count = result.score.cap_params.get("count", 1)
        yield result.score.cap_key, tn(result.score.cap_key, count, language, **result.score.cap_params)


@pytest.mark.parametrize("language", NON_ENGLISH)
def test_no_vocabulary_token_reaches_a_reader(analysed, language):
    leaked = []
    for key, text in _rendered(analysed, language):
        for token in VOCABULARY:
            if term(token, language) == token:
                # A few tokens are spelled the same in some languages --
                # "Master" in German, "master" in Dutch. Nothing to leak.
                continue
            # Whole words only: "phone" lives inside "telefoonnummer" and
            # "téléphone" without either being a leak.
            if re.search(rf"\b{re.escape(token)}\b", text):
                leaked.append(f"{key}: {token} in {text!r}")

    assert not leaked, f"{language} shows the code's words:\n" + "\n".join(leaked)


@pytest.mark.parametrize("language", NON_ENGLISH)
def test_nothing_renders_an_unresolved_placeholder(analysed, language):
    """A translation that renamed a placeholder, or a key with no entry,
    surfaces as a brace or a bracket rather than raising. Neither is
    findable by reading the source."""
    broken = [
        f"{key}: {text!r}"
        for key, text in _rendered(analysed, language)
        if "{" in text or text.startswith("[")
    ]

    assert not broken, f"{language} renders unfilled text:\n" + "\n".join(broken)


def test_the_fixture_actually_exercises_the_section_finding(analysed):
    """If the generator ever stops producing a section loss, both tests
    above would pass by having nothing to check."""
    ids = {finding.rule.id for finding in analysed.findings}

    assert "section_missing_under_naive_parsing" in ids
