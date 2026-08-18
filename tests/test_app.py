"""Smoke test for app.py using Streamlit's AppTest harness — confirms the
page loads without exceptions in its idle state (before any file is
uploaded). The actual extraction/rule-engine logic app.py calls is tested
thoroughly in test_pipeline.py; this just guards against the UI code itself
being broken (bad imports, typos in widget calls, etc.).
"""

from pathlib import Path

from streamlit.testing.v1 import AppTest

APP_PATH = str(Path(__file__).parent.parent / "app.py")


def test_app_loads_without_exception():
    at = AppTest.from_file(APP_PATH)
    at.run()

    assert not at.exception


def test_app_shows_title_and_uploader():
    at = AppTest.from_file(APP_PATH)
    at.run()

    assert at.title[0].value == "ATS Resume X-Ray"
    assert len(at.get("file_uploader")) == 1
