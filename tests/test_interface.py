"""The stylesheet and the theme config, which nothing else reads.

Two whole surfaces had no test at all: ``assets/app.css`` and
``.streamlit/config.toml``. Every interface defect found in review would
have been silently reintroduced, and two of them were the same mistake made
twice -- a selector written against a Streamlit internal that does not
exist, and a colour chosen against a ground it never sits on.

These are cheap, static checks. They cannot tell you a design is good; they
can tell you a rule is dead, a promise is broken or a value has drifted.
"""

import re
from pathlib import Path

import pytest

from ats_xray.overlay import SEVERITY_COLORS

ROOT = Path(__file__).parent.parent
CSS = (ROOT / "assets" / "app.css").read_text(encoding="utf-8")
CONFIG = (ROOT / ".streamlit" / "config.toml").read_text(encoding="utf-8")
APP = (ROOT / "app.py").read_text(encoding="utf-8")


def test_the_stylesheet_is_not_empty():
    """Everything below asserts an absence; without this they would all
    pass on a file that failed to load."""
    assert len(CSS) > 2000


def test_no_rule_depends_on_the_operating_system_theme():
    """@media (prefers-color-scheme) follows the OS, and Streamlit has its
    own light/dark toggle. A reader on a light OS who switched the app to
    dark got the light palette on a near-black ground -- 3.89:1 where small
    text needs 4.5. The palette is derived from currentColor instead."""
    assert "prefers-color-scheme" not in CSS


def test_no_emotion_class_is_targeted():
    """The file header promises this. Generated class names change between
    Streamlit releases and would break without a symptom."""
    generated = re.findall(r"\.st-emotion-cache[\w-]*", CSS)

    assert not generated, f"generated class names in the stylesheet: {generated}"


# Built as `stBaseButton-${kind}` in the frontend, so the whole string
# never appears in the bundle even though the attribute does.
TEMPLATED_TESTIDS = {"stBaseButton-primary", "stBaseButton-secondary"}


@pytest.fixture(scope="module")
def streamlit_bundle():
    import streamlit

    js = Path(streamlit.__file__).parent / "static" / "static" / "js"
    if not js.is_dir():
        pytest.skip("no Streamlit frontend build to check against")
    return "".join(path.read_text(encoding="utf-8", errors="ignore") for path in js.glob("*.js"))


def test_every_targeted_testid_exists_in_streamlit(streamlit_bundle):
    """A selector naming a data-testid that Streamlit does not emit is a
    rule that silently does nothing. The keyword chip rule was written
    against data-baseweb="tag", which 1.61 does not use, so a touch target
    that had supposedly been raised to 44px stayed at 28."""
    used = set(re.findall(r'\[data-testid="([\w-]+)"\]', CSS)) - TEMPLATED_TESTIDS
    missing = sorted(name for name in used if name not in streamlit_bundle)

    assert not missing, f"selectors for testids Streamlit does not emit: {missing}"


def test_every_targeted_data_attribute_exists_in_streamlit(streamlit_bundle):
    """Same trap, one level down: [data-tag] is real, [data-baseweb] is
    not."""
    used = {name for name in re.findall(r"\[(data-[\w-]+)[\]=]", CSS) if name != "data-testid"}
    missing = sorted(name for name in used if name not in streamlit_bundle)

    assert not missing, f"selectors for attributes Streamlit does not emit: {missing}"


EXACT_KEY_SELECTORS = set(re.findall(r'\.st-key-([\w-]+)[\s{,:\[]', CSS))
PREFIX_KEY_SELECTORS = set(re.findall(r'\[class\*="st-key-([\w-]+)"\]', CSS))


def _is_styled(key: str) -> bool:
    return key in EXACT_KEY_SELECTORS or any(
        key.startswith(prefix) for prefix in PREFIX_KEY_SELECTORS
    )


def test_every_container_key_is_styled():
    """A key exists so the stylesheet can reach the container. One that
    nothing selects is either dead weight or a rule that was renamed on one
    side only -- which is how four of the five split containers went on
    squeezing instead of stacking after the responsive rule was written."""
    keys = set(re.findall(r'st\.container\(key="([\w-]+)"\)', APP))
    unstyled = sorted(key for key in keys if not _is_styled(key))

    assert not unstyled, f"container keys no rule reaches: {unstyled}"


def test_every_styled_key_exists_in_the_app():
    keys = set(re.findall(r'key="([\w-]+)"', APP))
    orphans = sorted(
        selector
        for selector in EXACT_KEY_SELECTORS | PREFIX_KEY_SELECTORS
        if not any(key.startswith(selector) for key in keys)
    )

    assert not orphans, f"rules for containers the app never creates: {orphans}"


def _hex(rgb):
    return "#{:02X}{:02X}{:02X}".format(*rgb)


@pytest.mark.parametrize("severity", sorted(SEVERITY_COLORS))
def test_the_legend_matches_the_boxes_drawn_on_the_page(severity):
    """A legend swatch that is not the colour of the box it explains is
    worse than no legend. config.toml says these are "kept in step by
    hand", which is exactly the kind of promise that decays."""
    expected = _hex(SEVERITY_COLORS[severity])

    assert expected.lower() in CSS.lower(), f"{severity} swatch has drifted from overlay.py"
    assert expected.lower() in CONFIG.lower(), f"{severity} theme colour has drifted from overlay.py"


def test_streamlit_magic_is_off():
    """Streamlit renders any bare top-level expression, and a docstring
    under a module constant is one. Two were printing above the masthead on
    the live page."""
    assert re.search(r"^\s*magicEnabled\s*=\s*false", CONFIG, re.MULTILINE)


def test_no_module_docstring_can_reach_the_page():
    """The config setting is the mechanism; this is the symptom. A config
    reshuffle that dropped the setting would leave this failing."""
    for constant in ("PAGE_PANE_HEIGHT", "OUTCOME_PANE_HEIGHT"):
        assert f"{constant} = " in APP, f"{constant} is gone; update this test"

    assert "Tall enough for a whole A4 page" in APP, "the docstring under test has moved"


def test_touch_targets_are_declared_at_44px():
    """The three controls a thumb has to hit: the language menu, the jump
    links and the keyword-remove cross. All three were under 44px, and one
    of them stayed under it through a fix that claimed otherwise."""
    for selector in ('[data-testid="stPopoverButton"]',
                     ".st-key-language [data-testid=\"stRadioOption\"]",
                     '[data-testid="stMultiSelectTagsContainer"] span[data-tag]'):
        block = CSS.split(selector, 1)
        assert len(block) == 2, f"no rule for {selector}"
        assert "44px" in block[1][:200], f"{selector} does not declare a 44px target"


FSTRING_START = re.compile(r"""(?<![\w'"])(?:[fF][rRbB]?|[rRbB][fF])('''|\"\"\"|'|")""")


def _reuses_its_own_delimiter(source: str) -> list[int]:
    """Line numbers of f-strings that repeat their delimiter inside a
    replacement field.

    PEP 701 made that legal in 3.12. Before it, the string simply ends at
    the inner quote and the remainder is a syntax error.

    Hand-rolled rather than handed to ast.parse, because feature_version
    does not help here: it does not change how f-strings are tokenised, so
    a 3.12 interpreter accepts them however old a floor you ask it for.
    That is exactly why this class of mistake reaches CI.
    """
    found = []
    for match in FSTRING_START.finditer(source):
        delimiter = match.group(1)
        index, depth = match.end(), 0
        while index < len(source):
            char = source[index]
            if char == "\\":
                index += 2
                continue
            if char == "{":
                if source[index + 1 : index + 2] == "{":   # a literal brace
                    index += 2
                    continue
                depth += 1
            elif char == "}":
                depth = max(0, depth - 1)
            elif source.startswith(delimiter, index):
                if depth > 0:
                    found.append(source.count("\n", 0, index) + 1)
                break
            elif char == "\n" and len(delimiter) == 1:
                break
            index += 1
    return found


def test_no_f_string_reuses_its_own_quote():
    """This took CI down twice. A SyntaxError at import time is a
    collection error rather than a test result, so the run reports as every
    test failing at once and says nothing about which line. Both times the
    line worked perfectly on the 3.12 it was written on."""
    broken = []
    sources = (
        list((ROOT / "src").rglob("*.py"))
        + list((ROOT / "tests").rglob("*.py"))
        + [ROOT / "app.py"]
    )
    for path in sources:
        for line in _reuses_its_own_delimiter(path.read_text(encoding="utf-8")):
            broken.append(f"{path.relative_to(ROOT)}:{line}")

    assert not broken, "f-strings that need Python 3.12:\n" + "\n".join(broken)


def test_the_declared_python_floor_matches_what_the_code_needs():
    """pyproject said >=3.9 while ten modules annotate with `X | None` and
    none imports `from __future__ import annotations`. On 3.9 that installs
    cleanly and raises TypeError on the first import -- the worst shape a
    version constraint can have, because pip reports success."""
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    workflow = next((ROOT / ".github" / "workflows").glob("*.yml")).read_text(encoding="utf-8")

    declared = re.search(r'requires-python\s*=\s*">=(\d+)\.(\d+)"', pyproject)
    assert declared, "pyproject declares no python floor"
    floor = (int(declared.group(1)), int(declared.group(2)))

    tested = sorted(
        tuple(int(part) for part in version.split("."))
        for version in re.findall(r'"(\d+\.\d+)"', re.search(r"python-version:.*", workflow).group())
    )
    assert tested, "the workflow tests no python versions"
    assert floor == tested[0], (
        f"pyproject requires >={floor[0]}.{floor[1]} but CI's oldest is "
        f"{tested[0][0]}.{tested[0][1]}: one of them is untrue"
    )
