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

Every quantifier below has an explicit upper bound. Unbounded quantifiers
(``+``, ``{5,}``) on a character class that overlaps with "any character
that might appear before the required literal never actually shows up"
are a classic catastrophic-backtracking trap: on adversarial input (e.g.
a long run of letters with no ``@`` anywhere), an unbounded greedy match
gets re-attempted, and re-backtracked, at every single position in the
text, which is quadratic in input length. A resume-parsing tool that
accepts arbitrary uploaded text needs every regex bounded on principle,
not just the ones a test happens to catch.
"""

import re

_EMAIL_RE = re.compile(r"[a-zA-Z0-9_.+-]{1,64}@[a-zA-Z0-9-]{1,63}(?:\.[a-zA-Z0-9-]{1,63}){1,8}")
# The slash is in the class because German numbers are written
# "040 / 123 456 78". It also pulls date ranges like "09/2021 - 06/2025"
# in as single candidates, which the date shapes below then reject.
_PHONE_CANDIDATE_RE = re.compile(r"[+(]?\d[\d\s()/.-]{5,30}\d")
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


_DATE_SHAPES = (
    re.compile(r"^\d{1,2}[./]\d{1,2}[./]\d{2,4}$"),          # 12.03.1988
    re.compile(r"^\d{1,2}[./]\d{4}$"),                        # 09/2021
    re.compile(r"^\d{4}\s*[-–—]\s*\d{4}$"),                   # 2019 - 2024
    re.compile(r"^\d{1,2}[./]\d{4}\s*[-–—]\s*\d{1,2}[./]\d{4}$"),  # 09/2021 - 06/2025
    re.compile(r"^\d{4}\s*[-–—]\s*\d{1,4}$"),                 # 2024-0871, 2019-24
)
"""Shapes that are dates or reference numbers, never phone numbers.

A German Lebenslauf carries a date of birth and a column of employment
spans, and "12.03.1988" has eight digits and no letters -- indistinguishable
from a phone number by digit count alone. A CV with a date of birth and no
phone number at all was scoring 100/100 and being told both contact details
were found, which is the one failure this tool exists to catch."""

_PHONE_HINT = re.compile(r"^[+(]|^0|^00")
"""A real phone number written on a CV starts with a plus, a bracket or a
zero. Anything else needs enough digits that it cannot be a year."""

_MIN_DIGITS_WITHOUT_HINT = 9


def _looks_like_a_date(candidate: str) -> bool:
    return any(shape.match(candidate) for shape in _DATE_SHAPES)


def find_phone(text: str) -> str | None:
    for match in _PHONE_CANDIDATE_RE.finditer(text):
        candidate = match.group(0).strip()
        digit_count = sum(ch.isdigit() for ch in candidate)
        if not _MIN_PHONE_DIGITS <= digit_count <= _MAX_PHONE_DIGITS:
            continue
        if _looks_like_a_date(candidate):
            continue
        if not _PHONE_HINT.match(candidate) and digit_count < _MIN_DIGITS_WITHOUT_HINT:
            continue
        return candidate
    return None
