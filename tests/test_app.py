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
