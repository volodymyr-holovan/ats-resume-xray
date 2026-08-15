"""Contact-field extraction: name, email, phone — from already-extracted
resume text (works the same whether that text came from the PDF or DOCX
extractors, since it operates on plain text).

Name: the first non-empty line of text. Candidate names are almost
universally the very first thing on a resume, before any section headers.
This is a deliberately simple heuristic — it will misfire on templates that
put a decorative image or an address block above the name (see
``pdf_images``/``docx_structure`` for detecting those separately).

Email: a standard address-shaped regex.

Phone: any digit-heavy run of 7-15 digits, tolerant of spaces, dots,
dashes, and parentheses. The digit-count bounds exist to avoid matching
unrelated short numbers (a year, a bullet count) or absurdly long ones.
"""

import re

_EMAIL_RE = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
_PHONE_CANDIDATE_RE = re.compile(r"[+(]?\d[\d\s().-]{5,}\d")
_MIN_PHONE_DIGITS = 7
_MAX_PHONE_DIGITS = 15


def find_name(text: str) -> str | None:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return None


def find_email(text: str) -> str | None:
    match = _EMAIL_RE.search(text)
    return match.group(0) if match else None


def find_phone(text: str) -> str | None:
    for match in _PHONE_CANDIDATE_RE.finditer(text):
        candidate = match.group(0).strip()
        digit_count = sum(ch.isdigit() for ch in candidate)
        if _MIN_PHONE_DIGITS <= digit_count <= _MAX_PHONE_DIGITS:
            return candidate
    return None
