"""Section-header recognition: locates common resume section headers
(Experience, Education, Skills, ...) in extracted text and assigns the text
between one header and the next to that section.

Aliases are grouped by language so each language's list can be read and
corrected on its own; ``SECTION_ALIASES`` is the flattened view the rest of
the code matches against. Recognition is language-agnostic at run time --
a resume is matched against every language at once, so a CV that mixes
languages (an English heading over Ukrainian content, say) still resolves.

A line counts as a header only if, once normalized (trimmed, trailing
punctuation stripped, lowercased), it *equals* one of the known aliases --
not merely contains one. This deliberately excludes sentences that mention
a section word in passing (e.g. "My experience includes...") since those
are not standalone header lines. Lowercasing is Unicode-aware, so
"ОСВІТА", "Éducation" and "ÜBER MICH" all normalize correctly.
"""

import re

SECTION_ALIASES_BY_LANGUAGE: dict[str, dict[str, list[str]]] = {
    "en": {
        "experience": [
            "experience",
            "work experience",
            "professional experience",
            "employment history",
            "work history",
        ],
        "education": ["education", "academic background", "qualifications"],
        "skills": ["skills", "technical skills", "core competencies", "competencies"],
        "summary": ["summary", "profile", "professional summary", "about me", "objective"],
        "certifications": ["certifications", "certificates", "licenses"],
        "languages": ["languages"],
    },
    "de": {
        "experience": [
            "berufserfahrung",
            "praktische erfahrung",
            "werdegang",
            "beruflicher werdegang",
            "berufliche erfahrung",
        ],
        "education": ["ausbildung", "bildung", "schulbildung", "akademischer werdegang", "studium"],
        "skills": ["kenntnisse", "fähigkeiten", "kompetenzen", "fachkenntnisse"],
        "summary": ["profil", "über mich", "zusammenfassung", "kurzprofil"],
        "certifications": ["zertifikate", "zertifizierungen", "weiterbildung"],
        "languages": ["sprachen", "sprachkenntnisse"],
    },
    "uk": {
        "experience": [
            "досвід роботи",
            "досвід",
            "професійний досвід",
            "трудова діяльність",
        ],
        "education": ["освіта", "навчання"],
        "skills": ["навички", "ключові навички", "професійні навички", "компетенції", "уміння"],
        "summary": ["про себе", "профіль", "коротко про себе", "мета"],
        "certifications": ["сертифікати", "сертифікація", "курси"],
        "languages": ["мови", "знання мов", "володіння мовами"],
    },
    "ru": {
        "experience": [
            "опыт работы",
            "опыт",
            "профессиональный опыт",
            "трудовая деятельность",
        ],
        "education": ["образование", "обучение"],
        "skills": ["навыки", "ключевые навыки", "профессиональные навыки", "компетенции", "умения"],
        "summary": ["о себе", "профиль", "кратко о себе", "цель"],
        "certifications": ["сертификаты", "сертификация", "курсы"],
        "languages": ["языки", "знание языков", "владение языками"],
    },
    "es": {
        "experience": [
            "experiencia",
            "experiencia laboral",
            "experiencia profesional",
            "trayectoria profesional",
        ],
        "education": ["educación", "formación", "formación académica", "estudios"],
        "skills": ["habilidades", "competencias", "aptitudes", "conocimientos", "habilidades técnicas"],
        "summary": ["perfil", "sobre mí", "resumen", "perfil profesional", "objetivo"],
        "certifications": ["certificaciones", "certificados", "cursos"],
        "languages": ["idiomas", "lenguas"],
    },
    "nl": {
        "experience": ["werkervaring", "ervaring", "professionele ervaring", "loopbaan"],
        "education": ["opleiding", "opleidingen", "onderwijs", "studie"],
        "skills": ["vaardigheden", "competenties", "kwaliteiten", "technische vaardigheden"],
        "summary": ["profiel", "over mij", "samenvatting", "persoonlijk profiel", "doelstelling"],
        "certifications": ["certificaten", "certificeringen", "cursussen"],
        "languages": ["talen", "talenkennis"],
    },
    "fr": {
        "experience": [
            "expérience",
            "expérience professionnelle",
            "expériences professionnelles",
            "parcours professionnel",
        ],
        "education": ["formation", "éducation", "études", "parcours académique", "diplômes"],
        "skills": ["compétences", "compétences techniques", "savoir-faire", "aptitudes"],
        "summary": ["profil", "à propos", "résumé", "profil professionnel", "objectif"],
        "certifications": ["certifications", "certificats"],
        "languages": ["langues"],
    },
}

SUPPORTED_RESUME_LANGUAGES = tuple(SECTION_ALIASES_BY_LANGUAGE)


def _flatten() -> dict[str, list[str]]:
    """Collapse the per-language tables into section -> every alias.

    Duplicates across languages are real (French and English both use
    "certifications", German and French both use "profil"), and are kept
    once so a match reports the section rather than a language.
    """
    merged: dict[str, list[str]] = {}
    for language_table in SECTION_ALIASES_BY_LANGUAGE.values():
        for section, aliases in language_table.items():
            bucket = merged.setdefault(section, [])
            for alias in aliases:
                if alias not in bucket:
                    bucket.append(alias)
    return merged


SECTION_ALIASES: dict[str, list[str]] = _flatten()

_TRAILING_PUNCTUATION_RE = re.compile(r"[:\-–—]+$")


def find_section_headers(text: str) -> list[dict]:
    """Return recognized section headers as
    ``[{"section": str, "line_index": int, "raw_text": str}, ...]``, in the
    order they appear.
    """
    findings = []
    for index, line in enumerate(text.splitlines()):
        normalized = normalize_heading(line)
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


def normalize_heading(line: str) -> str:
    """Reduce a line to the form compared against SECTION_ALIASES: trimmed,
    trailing punctuation removed, lowercased. Public because locating a
    section on the page needs the same normalization the recognizer uses.
    """
    return _TRAILING_PUNCTUATION_RE.sub("", line.strip()).strip().lower()
