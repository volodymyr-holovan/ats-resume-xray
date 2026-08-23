"""Checking GitHub for a newer release.

The desktop build is a file someone downloaded once; without this it would
quietly go stale. On start it asks the GitHub releases API what the latest
tag is and compares it to the version baked into the build.

Everything here fails soft. A machine may be offline, behind a proxy, or
GitHub may be rate-limiting an unauthenticated request -- none of which is
a reason to stop someone analysing a resume, so every failure returns "no
update known" and the app carries on.
"""

import json
import re
import urllib.error
import urllib.request
from dataclasses import dataclass

from . import __version__

LATEST_RELEASE_API = "https://api.github.com/repos/volodymyr-holovan/ats-resume-xray/releases/latest"
RELEASES_PAGE = "https://github.com/volodymyr-holovan/ats-resume-xray/releases/latest"
REQUEST_TIMEOUT_SECONDS = 4

_VERSION_PART = re.compile(r"\d+")


@dataclass(frozen=True)
class UpdateInfo:
    current: str
    latest: str
    url: str


def parse_version(text: str) -> tuple[int, ...]:
    """Turn "v0.2.0" or "0.2" into a comparable tuple.

    Numeric parts only: a suffix like "-beta" is ignored rather than
    guessed at, since ordering pre-releases correctly is not something this
    needs to get right.
    """
    return tuple(int(part) for part in _VERSION_PART.findall(text)) or (0,)


def is_newer(latest: str, current: str) -> bool:
    """True when ``latest`` is a higher version than ``current``.

    Shorter tuples are padded, so 0.2 and 0.2.0 compare equal rather than
    reporting a phantom update every launch.
    """
    a, b = parse_version(latest), parse_version(current)
    length = max(len(a), len(b))
    return a + (0,) * (length - len(a)) > b + (0,) * (length - len(b))


def check_for_update(current_version: str = __version__) -> UpdateInfo | None:
    """Return details of a newer release, or None if this build is current
    or the check could not be completed.
    """
    try:
        request = urllib.request.Request(
            LATEST_RELEASE_API,
            headers={"Accept": "application/vnd.github+json", "User-Agent": "ats-resume-xray"},
        )
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            payload = json.load(response)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError):
        return None

    latest = (payload.get("tag_name") or "").strip()
    if not latest or not is_newer(latest, current_version):
        return None

    return UpdateInfo(
        current=current_version,
        latest=latest,
        url=payload.get("html_url") or RELEASES_PAGE,
    )
