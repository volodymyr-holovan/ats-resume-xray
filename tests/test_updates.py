import json
import urllib.error

import pytest

from ats_xray import __version__
from ats_xray.updates import check_for_update, is_newer, parse_version


def test_parse_version_ignores_the_v_prefix():
    assert parse_version("v0.2.0") == (0, 2, 0)


def test_parse_version_ignores_a_suffix():
    assert parse_version("1.4.2-beta") == (1, 4, 2)


def test_parse_version_of_junk_is_zero():
    assert parse_version("unreleased") == (0,)


def test_newer_version_is_detected():
    assert is_newer("v0.3.0", "0.2.0")
    assert is_newer("v1.0.0", "0.9.9")


def test_same_version_is_not_newer():
    assert not is_newer("v0.2.0", "0.2.0")


def test_differently_written_same_version_is_not_newer():
    """Padding matters: without it "0.2" would look older than "0.2.0" and
    the app would either nag or stay silent depending on how the tag was
    written.
    """
    assert not is_newer("v0.2", "0.2.0")
    assert not is_newer("v0.2.0", "0.2")


def test_older_release_does_not_trigger_an_update():
    assert not is_newer("v0.1.0", "0.2.0")


def _fake_response(payload):
    class Response:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self):
            return json.dumps(payload).encode()

    return Response()


def test_check_reports_a_newer_release(monkeypatch):
    import ats_xray.updates as module

    payload = {"tag_name": "v9.9.9", "html_url": "https://example.com/release"}
    monkeypatch.setattr(module.urllib.request, "urlopen", lambda *a, **k: _fake_response(payload))

    update = check_for_update("0.2.0")

    assert update is not None
    assert update.latest == "v9.9.9"
    assert update.current == "0.2.0"
    assert update.url == "https://example.com/release"


def test_check_is_quiet_when_up_to_date(monkeypatch):
    import ats_xray.updates as module

    monkeypatch.setattr(
        module.urllib.request, "urlopen", lambda *a, **k: _fake_response({"tag_name": "v0.2.0"})
    )

    assert check_for_update("0.2.0") is None


@pytest.mark.parametrize(
    "failure",
    [
        urllib.error.URLError("offline"),
        TimeoutError("slow"),
        OSError("socket died"),
    ],
)
def test_network_failures_never_surface(monkeypatch, failure):
    """Being offline, proxied or rate-limited is not a reason to stop
    someone analysing a resume, so every failure means "no update known".
    """
    import ats_xray.updates as module

    def boom(*args, **kwargs):
        raise failure

    monkeypatch.setattr(module.urllib.request, "urlopen", boom)

    assert check_for_update("0.2.0") is None


def test_malformed_response_never_surfaces(monkeypatch):
    import ats_xray.updates as module

    class Garbage:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self):
            return b"<html>not json</html>"

    monkeypatch.setattr(module.urllib.request, "urlopen", lambda *a, **k: Garbage())

    assert check_for_update("0.2.0") is None


def test_missing_tag_is_treated_as_no_update(monkeypatch):
    import ats_xray.updates as module

    monkeypatch.setattr(module.urllib.request, "urlopen", lambda *a, **k: _fake_response({}))

    assert check_for_update("0.2.0") is None


def test_package_version_is_parseable():
    """The bundled version feeds the comparison; if it were unparseable the
    desktop build would silently never see an update.
    """
    assert parse_version(__version__) > (0,)
