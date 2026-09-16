"""One CV per language, end to end, clean and with one seeded fault at a time.

Everything else in this suite tests a language through the part of the code
that obviously depends on it -- the section aliases, the skills lexicon, the
advert reader. Nothing ran a whole CV in all seven languages through the whole
pipeline, and the checks added most recently are the ones that needed it: a
convention check reads a document a parser is perfectly happy with, so its
only possible failure is a claim that is not true.

Which is what happened. Matching "ehrenamt" anywhere in the experience section
reported volunteering filed as employment on fourteen of eighty-one real
German applications, every one of which had put its volunteering in its own
section. The word was in a duty line -- the applicant had trained volunteers,
while being paid. The clean CVs here carry that line and the other traps that
came with it, and their job is to stay silent.

Latin-alphabet languages are rendered to PDF and Cyrillic ones to DOCX.
reportlab's built-in Helvetica has no Cyrillic glyphs and would write a page
of blanks, and reaching for a system font would tie the run to one machine.
Both extractors get exercised either way, which is worth having.
"""

import re

import docx
import pytest
from reportlab.pdfgen import canvas

import ats_xray.rules  # noqa: F401  (registers the rule set)
from ats_xray.conventions import analyze_conventions
from ats_xray.i18n import (
    RULE_DETAILS,
    RULE_FIXES,
    RULE_NAMES,
    RULE_PLAN,
    UI_LANGUAGES,
    t,
)
from ats_xray.langid import detect_language
from ats_xray.pipeline import analyze_path
from ats_xray.sections import find_section_headers

from cv_corpus import CLEAN, FAULTY, PARSING_FAULTS, TODAY

LANGUAGES = sorted(CLEAN)
UI = sorted(UI_LANGUAGES)
CYRILLIC = {"uk", "ru"}


def _write(directory, name: str, language: str, text: str):
    if language in CYRILLIC:
        path = directory / f"{name}.docx"
        document = docx.Document()
        for line in text.splitlines():
            document.add_paragraph(line)
        document.save(str(path))
        return path
    path = directory / f"{name}.pdf"
    page = canvas.Canvas(str(path), pagesize=(595, 842))
    page.setFont("Helvetica", 11)
    y = 790
    for line in text.splitlines():
        page.drawString(57, y, line)
        y -= 17
    page.save()
    return path


def _fired(text: str, language: str) -> dict:
    """``analyze_conventions`` keys every rule whether it fired or not."""
    hits = analyze_conventions(text, today=TODAY, language=language)
    return {rule: finding for rule, finding in hits.items() if finding is not None}


# --------------------------------------------------------------------------
# The corpus is what it claims to be
# --------------------------------------------------------------------------


@pytest.mark.parametrize("language", LANGUAGES)
def test_each_clean_cv_is_written_in_the_language_it_stands_for(language):
    """Otherwise the language-gated checks are all being skipped for the wrong
    reason and every assertion below passes without testing anything."""
    assert detect_language(CLEAN[language]) == language


@pytest.mark.parametrize("language", LANGUAGES)
def test_the_creative_headings_really_are_unrecognised(language):
    """The heading check only speaks up when nothing at all was recognised, so
    a replacement that happens to be in the vocabulary would leave the fault
    unseeded and the test green."""
    from cv_corpus import creative_headings

    assert find_section_headers(creative_headings(language)) == []


# --------------------------------------------------------------------------
# Silence on a clean document
# --------------------------------------------------------------------------


@pytest.mark.parametrize("language", LANGUAGES)
def test_a_clean_cv_reports_no_convention_problem(language):
    assert _fired(CLEAN[language], language) == {}


@pytest.mark.parametrize("language", LANGUAGES)
def test_a_clean_cv_parses_perfectly_through_the_whole_pipeline(language, tmp_path):
    path = _write(tmp_path, f"clean_{language}", language, CLEAN[language])
    result = analyze_path(str(path))
    assert [finding.rule.id for finding in result.findings] == []
    assert result.score.total == 100


# --------------------------------------------------------------------------
# One seeded fault, one finding
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "language,expected,text",
    FAULTY,
    ids=[f"{language}-{expected}" for language, expected, _ in FAULTY],
)
def test_a_seeded_convention_fault_reports_exactly_itself(language, expected, text):
    assert sorted(_fired(text, language)) == [expected]


@pytest.mark.parametrize(
    "language,expected,text",
    FAULTY,
    ids=[f"{language}-{expected}" for language, expected, _ in FAULTY],
)
def test_a_convention_fault_costs_no_score(language, expected, text, tmp_path):
    """The whole claim of ``rule.CONVENTION``: these are reported and not
    counted, because the score measures whether software can read the file and
    software has no difficulty with any of them."""
    path = _write(tmp_path, f"fault_{language}_{expected}", language, text)
    result = analyze_path(str(path))
    assert sorted(finding.rule.id for finding in result.findings) == [expected]
    assert result.score.total == 100


@pytest.mark.parametrize(
    "language,expected,text",
    PARSING_FAULTS,
    ids=[f"{language}-{expected}" for language, expected, _ in PARSING_FAULTS],
)
def test_a_seeded_parsing_fault_is_reported_and_does_cost_score(
    language, expected, text, tmp_path
):
    path = _write(tmp_path, f"parsing_{language}_{expected}", language, text)
    result = analyze_path(str(path))
    assert expected in [finding.rule.id for finding in result.findings]
    assert result.score.total < 100


# --------------------------------------------------------------------------
# What the reader is shown
# --------------------------------------------------------------------------

_UNFILLED = re.compile(r"[{}]")
_MISSING_KEY = re.compile(r"^\[.+\]$")
_BARE_IDENTIFIER = re.compile(r"(?<![\w/@.-])[a-z]+_[a-z_]+(?![\w/@.-])")

_EVIDENCE = sorted(
    {
        (expected, _fired(text, language)[expected].evidence_key)
        for language, expected, text in FAULTY
    }
)


@pytest.mark.parametrize("ui", UI)
def test_every_convention_evidence_sentence_renders_in_every_language(ui):
    """The existing leak test walks a two-column PDF, which produces parsing
    findings only, so these sentences and their parameters -- a count, a month,
    a line quoted from the CV -- had never been rendered by a test at all."""
    for language, expected, text in FAULTY:
        finding = _fired(text, language)[expected]
        rendered = t(finding.evidence_key, ui, **finding.params)
        assert not _MISSING_KEY.match(rendered), f"{finding.evidence_key} [{ui}] has no entry"
        assert not _UNFILLED.search(rendered), f"{finding.evidence_key} [{ui}]: {rendered}"
        leaked = _BARE_IDENTIFIER.findall(rendered)
        assert not leaked, f"{finding.evidence_key} [{ui}] leaked {leaked}: {rendered}"


@pytest.mark.parametrize("ui", UI)
@pytest.mark.parametrize("rule_id", sorted({rule for rule, _ in _EVIDENCE}))
def test_every_convention_rule_is_worded_in_every_language(rule_id, ui):
    """Asked of the tables rather than the accessors: the accessors fall back
    to English, so a missing translation reads as a present one."""
    for label, table in (
        ("name", RULE_NAMES),
        ("detail", RULE_DETAILS),
        ("fixes", RULE_FIXES),
        ("plan", RULE_PLAN),
    ):
        assert table.get(rule_id, {}).get(ui), f"{rule_id} has no {label} in {ui}"
