"""Faults that live in the text itself, whatever file it came out of.

The detectors in ``structure.py`` ask a PDF about its fonts and a DOCX
about its tables. These three ask the extracted text a question neither
file format can answer: is what a parser recovered actually usable?

They apply to both formats because the fault is not in the container. A
name written with a ligature is a broken word in a PDF and in a DOCX
alike, and a contact detail that exists only behind a hyperlink is
unreachable either way.
"""

import re

from .contact import find_email, find_phone
from .sections import find_section_headers

# --------------------------------------------------------------------------
# Contact details that exist only as a link
# --------------------------------------------------------------------------

PROFILE_HOSTS = ("linkedin.com", "xing.com", "github.com", "gitlab.com", "behance.net",
                 "dribbble.com", "stackoverflow.com", "researchgate.net", "orcid.org")

_MAILTO_RE = re.compile(r"mailto:", re.IGNORECASE)


def find_link_only_contact(text: str) -> list[str]:
    """Links that are the only way to reach the candidate, or [].

    A CV that writes "LinkedIn" as clickable text and no email is common
    and reads fine to a person: the link is right there. To a parser the
    link text is the word "LinkedIn", and the address behind it is an
    annotation most extractors never look at. The candidate has published
    a contact route the software cannot follow.

    Reported only when the plain-text route is genuinely absent, because a
    profile link *alongside* an email is just a profile link.
    """
    if find_email(text) and find_phone(text):
        return []

    found = []
    if _MAILTO_RE.search(text):
        found.append("mailto:")
    lowered = text.lower()
    for host in PROFILE_HOSTS:
        if host in lowered:
            found.append(host)
    if not found:
        return []

    # An email in the text means the address is reachable as text, whatever
    # else is linked; the same for a phone number.
    if find_email(text) or find_phone(text):
        return []
    return found


# --------------------------------------------------------------------------
# Headings a parser does not recognise
# --------------------------------------------------------------------------

MAX_HEADING_WORDS = 5
MAX_HEADING_CHARS = 60
MIN_HEADINGS = 2
_SENTENCE_END = re.compile(r"[.!?,;:]\s*$")
_HAS_DIGIT = re.compile(r"\d")


def find_unrecognised_headings(text: str) -> list[str]:
    """Lines that look like section headings but match no known vocabulary.

    The section detector works from a list of headings in seven languages.
    A CV that writes "My Journey" or "Was ich mitbringe" instead of
    "Experience" loses the section entirely — and the report then blames
    the layout, because "no sections found" is what a swallowed table looks
    like too. This separates the two: the content is readable, the labels
    are simply not ones the software knows.

    Only reported when *nothing* was recognised, and only from two upwards.
    A CV with "Experience" and one creative heading is fine — the parser
    has the anchor it needs — and a single heading-shaped line is far more
    likely to be a job title than a section label.
    """
    if find_section_headers(text):
        return []

    lines = text.splitlines()
    headings = []
    for index, line in enumerate(lines):
        stripped = line.strip()
        if not _is_heading_shaped(stripped):
            continue
        # White space above and content below. This is what separates a
        # heading from the name at the top of the page and from a job title
        # sitting in the middle of an entry -- the two things a looser test
        # reported, which would have been a worse finding than none.
        if index == 0 or lines[index - 1].strip():
            continue
        if not any(lines[after].strip() for after in range(index + 1, min(index + 3, len(lines)))):
            continue
        headings.append(stripped)
    return headings if len(headings) >= MIN_HEADINGS else []


def _is_heading_shaped(line: str) -> bool:
    if not line or len(line) > MAX_HEADING_CHARS:
        return False
    if _SENTENCE_END.search(line) or _HAS_DIGIT.search(line):
        return False
    # A comma is a list or an address -- "Studio Nord, Hamburg" is content,
    # however much it looks like a title.
    if "," in line:
        return False
    words = line.split()
    if not 1 <= len(words) <= MAX_HEADING_WORDS:
        return False
    if find_email(line) or find_phone(line):
        return False
    letters = [character for character in line if character.isalpha()]
    if not letters:
        return False
    # Either shouted or capitalised: the two ways a heading announces
    # itself without markup a parser can see.
    upper = sum(1 for character in letters if character.isupper())
    return upper == len(letters) or words[0][:1].isupper()


# --------------------------------------------------------------------------
# Characters that break a word without looking like it
# --------------------------------------------------------------------------

LIGATURES = {"ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl", "ﬃ": "ffi", "ﬄ": "ffl", "ﬅ": "ft", "ﬆ": "st"}
INVISIBLE = {
    "­": "soft hyphen",
    "​": "zero-width space",
    "‌": "zero-width non-joiner",
    "‍": "zero-width joiner",
    "﻿": "byte-order mark",
}

_CYRILLIC = re.compile(r"[Ѐ-ӿ]")
_LATIN = re.compile(r"[A-Za-z]")
_WORD = re.compile(r"[^\W\d_]+", re.UNICODE)


def find_broken_characters(text: str) -> list[str]:
    """Words a search will never match, with the reason, or [].

    Three things that look right on screen and are not the characters they
    appear to be:

    * a typographic ligature, where "ﬁ" is one character and a search for
      "fi" does not find it;
    * an invisible character — a soft hyphen left over from justified text,
      a zero-width space from a copy-paste — sitting inside a word;
    * a word mixing Latin and Cyrillic letters, which happens when someone
      types over an existing document with the wrong keyboard layout. This
      one is worth its own mention because the project shipped it: an alias
      in the skill list had a Cyrillic o in it and could never match.
    """
    found = []

    for ligature, plain in LIGATURES.items():
        if ligature in text:
            found.append(f"{ligature} ({plain})")

    for character, name in INVISIBLE.items():
        if character in text:
            found.append(name)

    for word in _WORD.findall(text):
        if _CYRILLIC.search(word) and _LATIN.search(word):
            found.append(f"{word} ({_describe_scripts(word)})")
            break  # one example is enough to make the point

    return found


def _describe_scripts(word: str) -> str:
    names = []
    for character in word:
        if not character.isalpha():
            continue
        script = "Cyrillic" if _CYRILLIC.match(character) else "Latin"
        if script not in names:
            names.append(script)
    return " + ".join(names)


def analyze_readability(text: str) -> dict:
    """Every text-level finding for one extraction."""
    return {
        "link_only_contact": find_link_only_contact(text),
        "unrecognised_headings": find_unrecognised_headings(text),
        "broken_characters": find_broken_characters(text),
    }


__all__ = [
    "analyze_readability",
    "find_broken_characters",
    "find_link_only_contact",
    "find_unrecognised_headings",
]
