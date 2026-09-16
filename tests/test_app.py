"""Smoke test for app.py using Streamlit's AppTest harness — confirms the
page loads without exceptions in its idle state (before any file is
uploaded). The actual extraction/rule-engine logic app.py calls is tested
thoroughly in test_pipeline.py; this just guards against the UI code itself
being broken (bad imports, typos in widget calls, etc.).
"""

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from ats_xray.i18n import UI_LANGUAGES, t
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


def test_app_shows_its_name_and_one_uploader():
    """The wordmark is drawn as markup rather than st.title so it can sit on
    one line with the tagline and the language control."""
    at = AppTest.from_file(APP_PATH)
    at.run()

    body = " ".join(markdown.value for markdown in at.markdown)
    assert "ATS Resume X-Ray" in body
    assert len(at.get("file_uploader")) == 1


def test_the_language_control_is_a_radio_in_the_masthead():
    """It used to be a selectbox in a collapsed sidebar, which most readers
    never opened -- six of the seven translations were unreachable."""
    at = AppTest.from_file(APP_PATH)
    at.run()

    languages = at.get("radio")
    assert languages, "no language control on the page"
    # The options carry the display names, which is what a reader picks from.
    assert set(languages[0].options) >= {"English", "Deutsch"}
    assert len(languages[0].options) == len(UI_LANGUAGES)


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
    at.get("radio")[0].set_value("uk").run()
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


def test_the_file_is_analysed_once_however_often_the_page_reruns(tmp_path, monkeypatch):
    """Every click reruns the whole script. Analysing and rendering the
    document again on each one made the page wait close to half a second to
    answer a language switch that had nothing to do with the file."""
    import ats_xray.pipeline as pipeline

    calls = []
    real = pipeline.analyze_bytes

    def counting(file_bytes, filename, render=False):
        calls.append(filename)
        return real(file_bytes, filename, render=render)

    monkeypatch.setattr(pipeline, "analyze_bytes", counting)

    resume = tmp_path / "resume.pdf"
    two_column_pdf(resume)
    at = AppTest.from_file(APP_PATH, default_timeout=120)
    at.run()
    _upload(at, resume)
    at.get("radio")[0].set_value("de").run()
    at.get("radio")[0].set_value("uk").run()

    assert not at.exception
    assert calls == ["resume.pdf"]
    # Still showing the analysis, in the language now chosen.
    assert t("details_expander", "uk") in [expander.label for expander in at.get("expander")]

    other = tmp_path / "other.pdf"
    _cv_pdf(other)
    _uploaded(at, other)
    assert calls == ["resume.pdf", "other.pdf"], "a different file must be analysed afresh"


PULL_UNDER_A_RUNNING_SERVER = r'''
import re, shutil, sys, time
from pathlib import Path
from streamlit.testing.v1 import AppTest

repo, sim, stamped = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3] == "stamped"
shutil.copytree(repo / "src", sim / "src", ignore=shutil.ignore_patterns("__pycache__"))
shutil.copytree(repo / "assets", sim / "assets")
shutil.copy2(repo / "app.py", sim / "app.py")

rule = sim / "src" / "ats_xray" / "rule.py"
current = rule.read_text(encoding="utf-8")
rule.write_text(re.sub(r"\nSEVERITY_ORDER = .*?\n", "\n", current), encoding="utf-8")
if not stamped:
    init = sim / "src" / "ats_xray" / "__init__.py"
    init.write_text(init.read_text(encoding="utf-8").replace("_IMPORTED_AT = _time.time()", ""), encoding="utf-8")

sys.path[:] = [p for p in sys.path if Path(p).resolve() != (repo / "src").resolve()]
for name in [n for n in sys.modules if n == "ats_xray" or n.startswith("ats_xray.")]:
    del sys.modules[name]
sys.path.insert(0, str(sim / "src"))
import ats_xray.rule
assert not hasattr(ats_xray.rule, "SEVERITY_ORDER"), "the simulated server should hold the old rule.py"

time.sleep(1.1)
rule.write_text(current, encoding="utf-8")

at = AppTest.from_file(str(sim / "app.py"), default_timeout=120)
at.run()
print("EXCEPTION" if at.exception else "RAN")
'''



@pytest.mark.parametrize("stamped", ["stamped", "unstamped"])
def test_the_page_survives_new_code_pulled_under_a_running_server(tmp_path, stamped):
    """The live page once raised ImportError on its first import from the
    package: a new app.py was running against an older rule.py still loaded in
    the server. Streamlit rereads app.py on every run but keeps an imported
    package as it was. "unstamped" is a server that loaded the package before
    it recorded its import time -- the one that was live when this was found.

    Run in a child process, because what is under test unloads modules and
    would do it to the test run too."""
    import subprocess
    import sys

    script = tmp_path / "pull.py"
    script.write_text(PULL_UNDER_A_RUNNING_SERVER, encoding="utf-8")
    root = Path(APP_PATH).parent
    result = subprocess.run(
        [sys.executable, str(script), str(root), str(tmp_path / "server"), stamped],
        capture_output=True, text=True, timeout=240,
    )

    assert result.returncode == 0, result.stderr[-2000:]
    assert result.stdout.strip().splitlines()[-1] == "RAN", result.stdout[-2000:]


def test_a_frozen_build_is_left_alone(tmp_path, monkeypatch):
    """The exe bundles ats_xray beside app.py, with no src directory. The
    check must not touch the path or unload anything there."""
    import ast
    import logging
    import sys

    source = Path(APP_PATH).read_text(encoding="utf-8")
    tree = ast.parse(source)
    check = next(node for node in tree.body
                 if isinstance(node, ast.FunctionDef) and node.name == "_load_this_commits_package")
    namespace = {"Path": Path, "sys": sys, "logger": logging.getLogger("frozen-test"),
                 "__file__": str(tmp_path / "app.py")}
    exec(compile(ast.Module(body=[check], type_ignores=[]), "app.py", "exec"), namespace)

    before_path = list(sys.path)
    before_modules = {name for name in sys.modules if name.startswith("ats_xray")}
    namespace["_load_this_commits_package"]()

    assert sys.path == before_path
    assert {name for name in sys.modules if name.startswith("ats_xray")} == before_modules
