"""Read a pasted job advert into a list of typed, weighted requirements.

Job adverts have a shape. A German one names its blocks -- "Ihre Aufgaben",
"Ihr Profil", "Wir bieten" -- and the blocks mean different things: the
profile block states requirements, the tasks block describes work and only
implies them, and the offer block is about the employer and contains no
requirements at all. Reading all three the same way is how keyword tools end
up telling candidates they are missing "Betriebliche Altersvorsorge".

Within a block, single phrases decide how hard a requirement is. "Zwingend
erforderlich" and "von Vorteil" sit in the same sentence structure and mean
opposite things, and German adverts use them consistently enough to read.
"""

from dataclasses import dataclass, field

from .credentials import (
    EDUCATION_RANK,
    education_waived,
    find_education,
    find_languages,
    find_licence,
    find_required_years,
    language_required_without_level,
)
from .langid import detect_language, merge_for
from .normalize import fold
from .skills_lexicon import find_skills, label_for
from .terms import MAX_TERMS_PER_AD, extract_terms

BLOCK_HEADINGS_BY_LANGUAGE: dict[str, dict[str, tuple[str, ...]]] = {
    "de": {
        # German adverts invent their own headings, and half of them address
        # the reader informally. "Zeichnet aus" alone covers "Das zeichnet
        # Sie aus", "Dich zeichnet aus" and "Was dich auszeichnet".
        "profile": ("ihr profil", "dein profil", "das bringen sie mit", "das bringst du mit", "was sie mitbringen", "was du mitbringst", "das solltest du mitbringen", "anforderungen", "anforderungsprofil", "qualifikationen", "ihre qualifikationen", "deine qualifikationen", "voraussetzungen", "unsere erwartungen", "zeichnet aus", "auszeichnet", "ueberzeugen sie uns", "ueberzeugst du uns", "ihr koennen", "dein koennen", "fachliche anforderungen", "wen wir suchen", "wen suchen wir", "das wuenschen wir uns", "ihr hintergrund"),
        "tasks": ("ihre aufgaben", "deine aufgaben", "aufgabengebiet", "taetigkeiten", "stellenbeschreibung", "ihre rolle", "deine rolle", "aufgabenschwerpunkte", "ihr taetigkeitsfeld", "diese aufgaben", "das sind ihre aufgaben", "das machst du"),
        # "Was Sie erwartet" reads as the offer far more often than as the
        # duties, and benefit lines mined as requirements are the more
        # visible mistake.
        "offer": ("wir bieten", "was wir bieten", "das bieten wir", "wir bieten dir", "wir bieten ihnen", "unsere benefits", "deine benefits", "ihre vorteile", "deine vorteile", "wir freuen uns", "unser angebot", "was wir ihnen bieten", "darauf koennen sie sich freuen", "darauf kannst du dich freuen", "was sie erwartet", "was dich erwartet", "das erwartet sie", "das erwartet dich", "in deinem neuen job", "in ihrem neuen job", "das bekommst du", "deine perspektiven", "unsere leistungen"),
    },
    "en": {
        "profile": ("your profile", "requirements", "what you bring", "qualifications", "about you", "your skills", "who you are", "what we expect"),
        "tasks": ("your tasks", "your responsibilities", "responsibilities", "the role", "what you will do", "job description", "your mission"),
        "offer": ("we offer", "what we offer", "our offer", "benefits", "perks", "why join us", "what is in it for you"),
    },
    "es": {
        "profile": ("tu perfil", "su perfil", "requisitos", "perfil del candidato", "que buscamos"),
        "tasks": ("tus tareas", "funciones", "responsabilidades", "descripcion del puesto"),
        "offer": ("ofrecemos", "que ofrecemos", "beneficios", "te ofrecemos"),
    },
    "nl": {
        "profile": ("jouw profiel", "uw profiel", "wat vragen wij", "functie-eisen", "vereisten", "wie ben jij"),
        "tasks": ("jouw taken", "werkzaamheden", "functieomschrijving", "wat ga je doen"),
        "offer": ("wij bieden", "wat bieden wij", "arbeidsvoorwaarden", "ons aanbod"),
    },
    "fr": {
        "profile": ("votre profil", "profil recherche", "exigences", "vos competences", "qui etes-vous"),
        "tasks": ("vos missions", "vos taches", "description du poste", "responsabilites"),
        "offer": ("nous offrons", "ce que nous offrons", "avantages", "notre offre"),
    },
    "uk": {
        "profile": ("ваш профіль", "вимоги", "наші вимоги", "що ми очікуємо", "кваліфікація"),
        "tasks": ("ваші завдання", "обов", "посадові обов", "опис вакансії"),
        "offer": ("ми пропонуємо", "що ми пропонуємо", "умови роботи", "переваги"),
    },
    "ru": {
        "profile": ("ваш профиль", "требования", "наши требования", "что мы ожидаем", "квалификация"),
        "tasks": ("ваши задачи", "обязанности", "должностные обязанности", "описание вакансии"),
        "offer": ("мы предлагаем", "что мы предлагаем", "условия работы", "преимущества"),
    },
}

BLOCK_ORDER = ("profile", "tasks", "offer")
"""Checked in this order, so a line matching two block names is read as the
more specific one."""


def _headings_for(language: str) -> dict[str, tuple[str, ...]]:
    merged: dict[str, list[str]] = {block: [] for block in BLOCK_ORDER}
    for code in (language, "en"):
        for block, headings in BLOCK_HEADINGS_BY_LANGUAGE.get(code, {}).items():
            merged[block].extend(headings)
    return {block: tuple(headings) for block, headings in merged.items()}


MUST_CUES_BY_LANGUAGE: dict[str, tuple[str, ...]] = {
    "de": ("zwingend", "zwingend erforderlich", "erforderlich", "voraussetzung", "voraussetzungen", "setzen wir voraus", "unabdingbar", "unerlaesslich", "notwendig", "muss", "muessen", "wird vorausgesetzt"),
    "en": ("required", "must have", "must-have", "mandatory", "essential", "is a must"),
    "es": ("imprescindible", "obligatorio", "requisito indispensable", "se requiere"),
    "nl": ("vereist", "noodzakelijk", "must", "verplicht"),
    "fr": ("exige", "obligatoire", "indispensable", "requis"),
    "uk": ("обов", "вимагається", "необхідн", "мусить"),
    "ru": ("обязательн", "требуется", "необходим"),
}

NICE_CUES_BY_LANGUAGE: dict[str, tuple[str, ...]] = {
    "de": ("von vorteil", "vorteilhaft", "wuenschenswert", "idealerweise", "im idealfall", "gerne auch", "ein plus", "pluspunkt", "optional", "von nutzen"),
    "en": ("nice to have", "nice-to-have", "a plus", "preferred", "desirable", "ideally", "bonus", "would be great", "an advantage"),
    "es": ("valorable", "deseable", "se valorara", "un plus"),
    "nl": ("een pre", "wenselijk", "gewenst", "is een plus"),
    "fr": ("un atout", "souhaite", "apprecie", "de preference"),
    "uk": ("буде перевагою", "бажано", "вітається", "як перевага"),
    "ru": ("будет преимуществом", "желательно", "приветствуется", "как плюс"),
}

MAX_HEADING_LENGTH = 80
"""A heading is short. Requiring that stops a sentence that happens to
contain "wir bieten" from splitting the advert in the wrong place."""


@dataclass(frozen=True)
class Requirement:
    """One thing the advert asks for.

    ``key`` is what the matcher compares on and ``label`` is what the reader
    sees and edits, because those are genuinely different: the key for a
    skill is a lexicon id, and for a degree it is a level name.
    """

    kind: str
    key: str
    label: str
    must: bool
    evidence: str = ""
    detail: dict = field(default_factory=dict)

    @property
    def uid(self) -> str:
        return f"{self.kind}:{self.key}"


@dataclass(frozen=True)
class VacancyProfile:
    requirements: tuple[Requirement, ...]
    blocks: dict[str, str]

    def by_kind(self, kind: str) -> list[Requirement]:
        return [r for r in self.requirements if r.kind == kind]


def split_blocks(text: str, language: str | None = None) -> dict[str, str]:
    """Group the advert's lines under the headings it uses.

    Text before the first recognised heading goes to ``"intro"``; an advert
    with no recognisable headings comes back as a single ``"profile"``
    block, because a pasted requirements list is the common case and
    treating it as an offer block would discard all of it.
    """
    language = language or detect_language(text)
    lines = text.splitlines()
    marks: list[tuple[int, str]] = []

    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped or len(stripped) > MAX_HEADING_LENGTH:
            continue
        folded = fold(stripped)
        for block, headings in _headings_for(language).items():
            # An empty folded heading would match every line; guard rather
            # than trust every alias to survive folding.
            if any(h and h in folded for h in (fold(heading) for heading in headings)):
                marks.append((index, block))
                break

    if not marks:
        return {"profile": text.strip()} if text.strip() else {}

    blocks: dict[str, list[str]] = {}
    intro = "\n".join(lines[: marks[0][0]]).strip()
    if intro:
        blocks["intro"] = [intro]

    for position, (line_index, block) in enumerate(marks):
        end = marks[position + 1][0] if position + 1 < len(marks) else len(lines)
        body = "\n".join(lines[line_index + 1 : end]).strip()
        if body:
            blocks.setdefault(block, []).append(body)

    return {name: "\n".join(parts) for name, parts in blocks.items()}


def line_is_must(line: str, default_must: bool, language: str = "en") -> bool:
    """Whether one line states a hard requirement.

    "Nice" is checked first on purpose. When a line carries both kinds of
    cue the softer reading is the safer error: a real must-have shown as
    preferred is a smaller problem for the reader than a preference shown
    as a blocking gap.
    """
    folded = fold(line)
    if any(fold(cue) in folded for cue in merge_for(NICE_CUES_BY_LANGUAGE, language)):
        return False
    if any(fold(cue) in folded for cue in merge_for(MUST_CUES_BY_LANGUAGE, language)):
        return True
    return default_must


BLOCK_DEFAULT_MUST = {"profile": True, "tasks": False, "intro": False}
SCANNED_BLOCKS = ("profile", "tasks", "intro")
"""The offer block is never scanned. Everything in it is what the employer
gives, not what the candidate needs."""


def _blocks_worth_scanning(blocks: dict[str, str]) -> dict[str, str]:
    """The parts of the advert that can state a requirement.

    The intro is only worth reading when the advert has no labelled blocks
    at all -- someone who pasted a bare requirements list. In an advert that
    does label its blocks, the intro is the company describing itself, and
    mining it produces exactly the nouns you would expect: the hospital's
    name, its district, its bed count and its founding order.
    """
    if "profile" not in blocks:
        # No requirements block was recognised, so they are somewhere in the
        # text this parser did not label. Dropping the intro here would throw
        # away the only place they can be, which is how an advert headed
        # "Dich zeichnet aus" came back with no requirements at all.
        return {name: body for name, body in blocks.items() if name in SCANNED_BLOCKS}
    return {name: body for name, body in blocks.items() if name in ("profile", "tasks")}


def parse_vacancy(text: str, language: str | None = None) -> VacancyProfile:
    """Read an advert into weighted requirements.

    The language is detected once and every phrase vocabulary is narrowed to
    it plus English, because an advert and the CV measured against it are
    written in one language and reading all seven invites cross-language
    false positives.
    """
    language = language or detect_language(text)
    blocks = split_blocks(text, language)
    scanned = _blocks_worth_scanning(blocks)
    requirements: dict[str, Requirement] = {}

    def add(requirement: Requirement) -> None:
        existing = requirements.get(requirement.uid)
        # A skill named in both the profile and the tasks block keeps the
        # harder reading: the advert asked for it twice.
        if existing is None or (requirement.must and not existing.must):
            requirements[requirement.uid] = requirement

    for name, body in scanned.items():
        default_must = BLOCK_DEFAULT_MUST.get(name, False)
        for line in body.splitlines():
            if not line.strip():
                continue
            must = line_is_must(line, default_must, language)
            for skill_id in find_skills(line):
                add(
                    Requirement(
                        kind="skill",
                        key=skill_id,
                        label=label_for(skill_id),
                        must=must,
                        evidence=line.strip(),
                    )
                )
            # Anything the lexicon does not know still has to surface, or an
            # advert for a trade nobody added would produce an empty list.
            for term in extract_terms(line, language):
                add(
                    Requirement(
                        kind="skill",
                        key=f"term:{fold(term)}",
                        label=term,
                        must=must,
                        evidence=line.strip(),
                    )
                )
            years = find_required_years(line, language)
            if years:
                add(
                    Requirement(
                        kind="experience",
                        key="years",
                        label=f"{years}+ Jahre / years",
                        must=must,
                        evidence=line.strip(),
                        detail={"years": years},
                    )
                )

    _add_education(scanned, text, add, language)
    _add_languages(scanned, add, language)

    licence = find_licence(text)
    if licence:
        add(
            Requirement(
                kind="licence",
                key=licence,
                label=f"Führerschein / licence {licence}",
                must=_licence_is_must(text, language),
                evidence=_line_containing(text, "hrerschein") or _line_containing(text, "licence") or "",
            )
        )

    _cap_generic_terms(requirements)

    ordered = sorted(
        requirements.values(),
        key=lambda r: (not r.must, KIND_ORDER.get(r.kind, 9), r.label.lower()),
    )
    return VacancyProfile(tuple(ordered), blocks)


def _cap_generic_terms(requirements: dict) -> None:
    """Keep the guessed keywords to a readable number.

    Lexicon hits are never dropped: those are known skills. Only the
    generic guesses are trimmed, required ones first, because a list too
    long to read is a list nobody will correct.
    """
    generic = [r for r in requirements.values() if r.key.startswith("term:")]
    if len(generic) <= MAX_TERMS_PER_AD:
        return
    keep = {r.uid for r in sorted(generic, key=lambda r: not r.must)[:MAX_TERMS_PER_AD]}
    for requirement in generic:
        if requirement.uid not in keep:
            del requirements[requirement.uid]


KIND_ORDER = {"education": 0, "experience": 1, "language": 2, "licence": 3, "skill": 4}


def _add_education(scanned: dict[str, str], whole_text: str, add, language: str) -> None:
    if education_waived(whole_text, language):
        return
    best: Requirement | None = None
    for name, body in scanned.items():
        default_must = BLOCK_DEFAULT_MUST.get(name, False)
        for line in body.splitlines():
            fact = find_education(line, language)
            if fact is None:
                continue
            candidate = Requirement(
                kind="education",
                key=fact.level,
                label=_education_label(fact.level),
                must=line_is_must(line, default_must, language) and not fact.equivalent_accepted,
                evidence=line.strip(),
                detail={
                    "level": fact.level,
                    "field": fact.field,
                    "equivalent_accepted": fact.equivalent_accepted,
                },
            )
            if best is None or EDUCATION_RANK[fact.level] > EDUCATION_RANK[best.key]:
                best = candidate
    if best is not None:
        add(best)


EDUCATION_LABELS = {
    "ausbildung": "Ausbildung / vocational training",
    "bachelor": "Bachelor / Studium",
    "master": "Master / Diplom",
    "doctorate": "Promotion / doctorate",
}


def _education_label(level: str) -> str:
    return EDUCATION_LABELS.get(level, level)


def _add_languages(scanned: dict[str, str], add, language: str) -> None:
    body = "\n".join(scanned.values())
    if not body.strip():
        return

    for fact in find_languages(body, language):
        add(
            Requirement(
                kind="language",
                key=fact.language,
                label=f"{fact.language.upper()} {fact.level.upper()}",
                must=True,
                evidence=fact.evidence,
                detail={"level": fact.level},
            )
        )

    for code in language_required_without_level(body, language):
        add(
            Requirement(
                kind="language",
                key=code,
                label=f"{code.upper()}",
                must=False,
                evidence="",
                detail={"level": None},
            )
        )


def _licence_is_must(text: str, language: str = "en") -> bool:
    line = _line_containing(text, "hrerschein") or _line_containing(text, "licence")
    return line_is_must(line, True, language) if line else True


def _line_containing(text: str, needle: str) -> str | None:
    lowered = needle.lower()
    for line in text.splitlines():
        if lowered in line.lower():
            return line.strip()
    return None
