"""Section-header recognition: locates common resume section headers
(Experience, Education, Skills, ...) in extracted text, in English and
German, and assigns the text between one header and the next to that
section.

A line counts as a header only if, once normalized (trimmed, trailing
punctuation stripped, lowercased), it *equals* one of the known aliases —
not merely contains one. This deliberately excludes sentences that mention
a section word in passing (e.g. "My experience includes...") since those
are not standalone header lines.
"""

import re

SECTION_ALIASES: dict[str, list[str]] = {
    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "work history",
        "berufserfahrung",
        "praktische erfahrung",
        "werdegang",
        "beruflicher werdegang",
    ],
    "education": [
        "education",
        "academic background",
        "ausbildung",
        "bildung",
        "schulbildung",
        "akademischer werdegang",
    ],
    "skills": [
        "skills",
        "technical skills",
        "core competencies",
        "competencies",
        "kenntnisse",
        "fähigkeiten",
        "kompetenzen",
    ],
    "summary": [
        "summary",
        "profile",
        "professional summary",
        "about me",
        "objective",
        "profil",
        "über mich",
        "zusammenfassung",
    ],
    "certifications": [
        "certifications",
        "certificates",
        "licenses",
        "zertifikate",
        "zertifizierungen",
    ],
    "languages": [
        "languages",
        "sprachen",
        "sprachkenntnisse",
    ],
}

_TRAILING_PUNCTUATION_RE = re.compile(r"[:\-–—]+$")


def find_section_headers(text: str) -> list[dict]:
    """Return recognized section headers as
    ``[{"section": str, "line_index": int, "raw_text": str}, ...]``, in the
    order they appear.
    """
    findings = []
    for index, line in enumerate(text.splitlines()):
        normalized = _normalize_header(line)
        if not normalized:
            continue
        for section, aliases in SECTION_ALIASES.items():
            if normalized in aliases:
                findings.append({"section": section, "line_index": index, "raw_text": line.strip()})
                break
    return findings


def split_into_sections(text: str) -> dict[str, str]:
    """Split text into sections based on recognized headers: each section's
    content is every line between its header and the next recognized
    header (or end of text). Text before the first recognized header is
    returned under the ``"preamble"`` key (typically name/contact info at
    the top of the resume). If no headers are recognized at all, the whole
    text is returned as ``"preamble"``.
    """
    lines = text.splitlines()
    headers = find_section_headers(text)

    if not headers:
        return {"preamble": text.strip()}

    sections: dict[str, str] = {}

    preamble = "\n".join(lines[: headers[0]["line_index"]]).strip()
    if preamble:
        sections["preamble"] = preamble

    for i, header in enumerate(headers):
        start = header["line_index"] + 1
        end = headers[i + 1]["line_index"] if i + 1 < len(headers) else len(lines)
        content = "\n".join(lines[start:end]).strip()
        if header["section"] in sections:
            sections[header["section"]] = f'{sections[header["section"]]}\n{content}'.strip()
        else:
            sections[header["section"]] = content

    return sections


def _normalize_header(line: str) -> str:
    return _TRAILING_PUNCTUATION_RE.sub("", line.strip()).strip().lower()
