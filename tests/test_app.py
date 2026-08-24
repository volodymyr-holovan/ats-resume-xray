"""Smoke test for app.py using Streamlit's AppTest harness — confirms the
page loads without exceptions in its idle state (before any file is
uploaded). The actual extraction/rule-engine logic app.py calls is tested
thoroughly in test_pipeline.py; this just guards against the UI code itself
being broken (bad imports, typos in widget calls, etc.).
"""

from pathlib import Path

from streamlit.testing.v1 import AppTest

from ats_xray.i18n import t
from golden_generators import two_column_pdf

APP_PATH = str(Path(__file__).parent.parent / "app.py")


def _upload(at, path):
    at.get("file_uploader")[0].set_value(
        (path.name, path.read_bytes(), "application/pdf")
    )
    return at.run()


def test_app_loads_without_exception():
    at = AppTest.from_file(APP_PATH)
    at.run()

    assert not at.exception


def test_app_shows_title_and_uploader():
    at = AppTest.from_file(APP_PATH)
    at.run()

    assert at.title[0].value == "ATS Resume X-Ray"
    assert len(at.get("file_uploader")) == 1


def test_app_offers_details_and_fixes_under_each_finding(tmp_path):
    """The headline names the problem; everything needed to act on it sits
    one click below. This checks the click has something behind it."""
    resume = tmp_path / "resume.pdf"
    two_column_pdf(resume)

    at = AppTest.from_file(APP_PATH, default_timeout=120)
    at.run()
    _upload(at, resume)

    assert not at.exception
    labels = [expander.label for expander in at.get("expander")]
    assert t("details_expander", "en") in labels

    body = " ".join(markdown.value for markdown in at.markdown)
    assert t("how_to_fix", "en") in body
    assert "1. " in body


def test_app_source_link_points_at_the_file_in_the_displayed_language(tmp_path):
    """Reading a finding in Ukrainian and then being handed an English
    reference wastes the translation."""
    resume = tmp_path / "resume.pdf"
    two_column_pdf(resume)

    at = AppTest.from_file(APP_PATH, default_timeout=120)
    at.run()
    at.get("selectbox")[0].set_value("uk").run()
    _upload(at, resume)

    assert not at.exception
    captions = " ".join(caption.value for caption in at.caption)
    assert "docs/research_sources.uk.md" in captions
    assert "blob/master/research_sources.md" not in captions


GERMAN_AD = """Ihr Profil
- Abgeschlossenes Studium der Informatik oder vergleichbare Qualifikation
- Mindestens 2 Jahre Berufserfahrung
- Kenntnisse in SQL sind zwingend erforderlich
- Erfahrung mit Docker von Vorteil

Wir bieten
- Weiterbildung mit Kubernetes-Schulungen
"""


def _cv_pdf(path):
    """A single-column CV with the sections the matcher scopes on: dates
    only count inside Berufserfahrung, degrees only inside Ausbildung."""
    from reportlab.pdfgen import canvas

    c = canvas.Canvas(str(path), pagesize=(520, 440))
    c.setFont("Helvetica", 11)
    lines = [
        "Jane Doe",
        "jane@example.com  +49 160 4562730",
        "",
        "Ausbildung",
        "Bachelor of Science, Informatik",
        "Technische Universitaet, 09/2021 - 06/2025",
        "",
        "Berufserfahrung",
        "Technischer Support, 09/2023 - 06/2026",
        "Betrieb und Wartung von Technik",
        "",
        "Kenntnisse",
        "Python, SQL, Docker, Linux, Git",
        "",
        "Sprachen",
        "Deutsch - B2, Englisch - C1",
    ]
    for offset, line in enumerate(lines):
        c.drawString(30, 410 - offset * 18, line)
    c.save()


def _uploaded(at, path):
    at.get("file_uploader")[0].set_value((path.name, path.read_bytes(), "application/pdf"))
    return at.run()


def test_the_match_section_stays_out_of_the_way_until_an_ad_is_pasted():
    """Everything that worked before has to keep working untouched for
    someone who only wants the parse report."""
    at = AppTest.from_file(APP_PATH, default_timeout=180)
    at.run()

    assert not at.exception
    assert len(at.get("text_area")) == 1
    assert not at.get("multiselect")


def test_keywords_are_extracted_from_a_pasted_ad_and_can_be_edited(tmp_path):
    resume = tmp_path / "cv.pdf"
    _cv_pdf(resume)

    at = AppTest.from_file(APP_PATH, default_timeout=180)
    at.run()
    _uploaded(at, resume)
    at.get("text_area")[0].set_value(GERMAN_AD).run()

    assert not at.exception
    required, preferred = at.get("multiselect")[0], at.get("multiselect")[1]
    assert "SQL" in required.value
    assert "Docker" in preferred.value
    # The offer block is not a requirements list.
    assert "Kubernetes" not in required.value + preferred.value


def test_scoring_runs_only_after_the_button_and_reports_a_match(tmp_path):
    resume = tmp_path / "cv.pdf"
    _cv_pdf(resume)

    at = AppTest.from_file(APP_PATH, default_timeout=180)
    at.run()
    _uploaded(at, resume)
    at.get("text_area")[0].set_value(GERMAN_AD).run()

    assert len(at.get("metric")) == 1, "no match score before the button is pressed"

    next(b for b in at.get("button") if t("match_evaluate_button", "en") in b.label).click().run()

    assert not at.exception
    labels = [m.label for m in at.get("metric")]
    assert any(t(key, "en") in labels for key in ("match_rating_strong", "match_rating_good"))


def test_a_keyword_typed_by_the_reader_is_scored_too(tmp_path):
    """The editable list is the point: extraction is a guess, and the
    reader has to be able to add what the ad only implied."""
    resume = tmp_path / "cv.pdf"
    _cv_pdf(resume)

    at = AppTest.from_file(APP_PATH, default_timeout=180)
    at.run()
    _uploaded(at, resume)
    at.get("text_area")[0].set_value(GERMAN_AD).run()

    required = at.get("multiselect")[0]
    required.set_value(list(required.value) + ["Kernphysik"]).run()
    next(b for b in at.get("button") if t("match_evaluate_button", "en") in b.label).click().run()

    assert not at.exception
    body = " ".join(m.value for m in at.markdown)
    assert "Kernphysik" in body
