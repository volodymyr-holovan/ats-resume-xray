"""Five graded CVs and the five adverts they were written against.

Every other fixture in this suite isolates one fault, which makes each a
good unit fixture and poor evidence. A real CV is never one problem, and
the question that matters is whether the tool ranks two imperfect
documents the way a person would.

What is asserted here, and what deliberately is not:

* **Parse readiness is ordered.** It measures one thing for any document,
  so the five are comparable and the score has to rise from the worst to
  the best. This is the assertion that breaks when a detector regresses.
* **Match is not ordered.** Each CV is measured against a *different*
  advert, so comparing the numbers across the corpus would be comparing
  two different questions. The match assertions are per-CV instead: this
  one is missing the licence the advert insists on, that one has met every
  requirement.

The adverts are original text written after reading real listings, not
copies of them — see ``corpus/vacancies/README.md``.
"""

from pathlib import Path

import pytest

import ats_xray.rules  # noqa: F401  (registers the rule set)
from ats_xray.match import evaluate_match
from ats_xray.pipeline import analyze_bytes
from ats_xray.vacancy import parse_vacancy

from corpus_generators import GRADED

VACANCIES = Path(__file__).parent / "corpus" / "vacancies"


@pytest.fixture(scope="module")
def corpus(tmp_path_factory):
    """Every CV analysed once, paired with its advert's match report."""
    directory = tmp_path_factory.mktemp("corpus")
    analysed = {}
    for name, vacancy, build, suffix in GRADED:
        path = directory / f"{name}{suffix}"
        build(path)
        result = analyze_bytes(path.read_bytes(), path.name)
        profile = parse_vacancy((VACANCIES / f"{vacancy}.txt").read_text(encoding="utf-8"))
        analysed[name] = (
            result,
            evaluate_match(profile.requirements, result.aware_text, result.naive_text),
        )
    return analysed


ORDER = [name for name, _, _, _ in GRADED]


def test_parse_readiness_rises_from_worst_to_best(corpus):
    """The one number comparable across the corpus, and the reason the
    corpus is graded rather than labelled."""
    scores = [corpus[name][0].score.total for name in ORDER]

    assert scores == sorted(scores), dict(zip(ORDER, scores))
    assert scores[0] < scores[-1] - 50, "the ends should be nowhere near each other"


def test_the_best_cv_has_nothing_to_report(corpus):
    """The control at the top end. Any finding here is a false positive:
    no table, no column, no image, no header, both contact fields in plain
    text, every heading one the parser knows."""
    result, report = corpus["5_best_software"]

    assert [f.rule.id for f in result.findings] == []
    assert result.score.total == 100
    assert report.missing_must == ()


def test_the_worst_cv_fails_in_several_ways_at_once(corpus):
    """Not one fault: the shape a visual template produces. A table holding
    the whole document, a contact line that is only a link, invented
    headings, and a ligature the exporter inserted."""
    result, _ = corpus["1_worst_care"]
    triggered = {f.rule.id for f in result.findings}

    assert {"docx_table_content", "contact_only_as_link", "broken_characters"} <= triggered
    assert result.score.total < 40


@pytest.mark.parametrize(
    "name,rule_id",
    [
        ("2_poor_logistics", "section_missing_under_naive_parsing"),
        ("2_poor_logistics", "pdf_repeated_header_footer_content"),
        ("1_worst_care", "missing_contact_field"),
    ],
)
def test_each_planted_fault_is_found(corpus, name, rule_id):
    """The faults were put there on purpose. A corpus that stops detecting
    them is a corpus that has stopped being evidence."""
    result, _ = corpus[name]

    assert rule_id in {f.rule.id for f in result.findings}


@pytest.mark.parametrize("name", ["3_middling_retail", "4_good_design", "5_best_software"])
def test_a_cleanly_built_cv_is_left_alone(corpus, name):
    """Three plain single-column PDFs. Whatever is wrong with them is on
    the content side, and the structural rules must stay quiet about it —
    a tool that finds something in every file teaches people to ignore it."""
    result, _ = corpus[name]

    assert [f.rule.id for f in result.findings] == []


# --------------------------------------------------------------------------
# The match, one advert at a time
# --------------------------------------------------------------------------


def test_the_logistics_cv_is_missing_the_licence_the_advert_insists_on(corpus):
    """Written that way: the layout faults are the visible half, and the
    forklift licence is the one that actually costs the application."""
    _, report = corpus["2_poor_logistics"]
    missing = {o.requirement.key for o in report.missing_must}

    assert "staplerschein" in {o.requirement.key.lower() for o in report.missing_must} or any(
        "stapler" in o.requirement.label.lower() for o in report.missing_must
    ), missing


def test_the_design_cv_is_told_what_to_add_first(corpus):
    """One gap, marked in the advert as a preference. The gains list should
    name it and price it below what a required item would be worth."""
    _, report = corpus["4_good_design"]

    assert report.gains, "a CV with a gap should be told which gap"
    assert all(points <= 20 for _, points in report.gains), "no must-have is missing here"


def test_the_worst_cv_still_matches_something(corpus):
    """A badly built file can hold the right words. Parse readiness and
    match answer different questions, and this is the case that proves it:
    the document is barely readable and the candidate is qualified."""
    _, report = corpus["1_worst_care"]

    assert report.score > 0
    assert report.of_status("met"), "the care vocabulary is there to be found"


def test_a_skill_last_used_a_decade_ago_is_flagged(corpus):
    """The logistics CV names its warehouse software in a job that ended in
    2012. Matched, and worth a question."""
    _, report = corpus["2_poor_logistics"]

    assert report.stale, "an entry that ended in 2012 should read as stale"


# --------------------------------------------------------------------------
# The adverts themselves
# --------------------------------------------------------------------------


@pytest.mark.parametrize("path", sorted(VACANCIES.glob("*.txt")), ids=lambda p: p.stem)
def test_every_advert_yields_hard_and_soft_requirements(path):
    """An advert that produces only preferences has not been read: German
    adverts separate the two by cue phrase, and every one of these uses
    them."""
    profile = parse_vacancy(path.read_text(encoding="utf-8"))

    assert any(r.must for r in profile.requirements), f"{path.stem}: no hard requirement"
    assert any(not r.must for r in profile.requirements), f"{path.stem}: no preference"


def test_the_advert_asking_for_five_years_is_read_as_five():
    """It says "mehrjährige Erfahrung" on one line and "mindestens 5 Jahre"
    on another. First-wins read the vague phrase, worth three by
    convention, and reported three."""
    profile = parse_vacancy((VACANCIES / "python_engineer.txt").read_text(encoding="utf-8"))
    years = [r.detail["years"] for r in profile.requirements if r.kind == "experience"]

    assert years == [5]


def test_a_shipping_container_is_not_docker():
    """"Be- und Entladen von LKW und Containern" is a loading bay. The
    lexicon read it as a container runtime until this corpus was written."""
    profile = parse_vacancy((VACANCIES / "lagerlogistik.txt").read_text(encoding="utf-8"))

    assert "docker" not in {r.key for r in profile.requirements}
