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
from .normalize import fold
from .skills_lexicon import find_skills, label_for

BLOCK_HEADINGS: dict[str, tuple[str, ...]] = {
    "profile": (
        "ihr profil",
        "dein profil",
        "das bringen sie mit",
        "das bringst du mit",
        "was sie mitbringen",
        "was du mitbringst",
        "anforderungen",
        "anforderungsprofil",
        "qualifikationen",
        "ihre qualifikationen",
        "voraussetzungen",
        "unsere erwartungen",
        "das zeichnet sie aus",
        "damit ueberzeugen sie uns",
        "your profile",
        "requirements",
        "what you bring",
        "qualifications",
        "about you",
        "your skills",
        "who you are",
        "perfil",
        "tu perfil",
        "jouw profiel",
        "votre profil",
        "ваш профіль",
        "ваш профиль",
    ),
    "tasks": (
        "ihre aufgaben",
        "deine aufgaben",
        "aufgabengebiet",
        "ihr aufgabengebiet",
        "taetigkeiten",
        "ihre taetigkeiten",
        "was sie erwartet",
        "was dich erwartet",
        "stellenbeschreibung",
        "your tasks",
        "your responsibilities",
        "responsibilities",
        "the role",
        "what you will do",
        "job description",
        "tus tareas",
        "jouw taken",
        "vos missions",
        "ваші завдання",
        "ваши задачи",
    ),
    "offer": (
        "wir bieten",
        "was wir bieten",
        "das bieten wir",
        "unsere benefits",
        "benefits",
        "ihre vorteile",
        "deine vorteile",
        "wir freuen uns",
        "unser angebot",
        "was wir ihnen bieten",
        "we offer",
        "what we offer",
        "our offer",
        "perks",
        "why join us",
        "ofrecemos",
        "wij bieden",
        "nous offrons",
        "ми пропонуємо",
        "мы предлагаем",
    ),
}

MUST_CUES = (
    "zwingend",
    "zwingend erforderlich",
    "erforderlich",
    "voraussetzung",
    "voraussetzungen",
    "setzen wir voraus",
    "unabdingbar",
    "unerlaesslich",
    "notwendig",
    "muss",
    "muessen",
    "required",
    "must have",
    "must-have",
    "mandatory",
    "essential",
)

NICE_CUES = (
    "von vorteil",
    "vorteilhaft",
    "wuenschenswert",
    "idealerweise",
    "im idealfall",
    "gerne auch",
    "ein plus",
    "pluspunkt",
    "optional",
    "nice to have",
    "nice-to-have",
    "a plus",
    "preferred",
    "desirable",
    "ideally",
    "bonus",
    "would be great",
)

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


def split_blocks(text: str) -> dict[str, str]:
    """Group the advert's lines under the headings it uses.

    Text before the first recognised heading goes to ``"intro"``; an advert
    with no recognisable headings comes back as a single ``"profile"``
    block, because a pasted requirements list is the common case and
    treating it as an offer block would discard all of it.
    """
    lines = text.splitlines()
    marks: list[tuple[int, str]] = []

    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped or len(stripped) > MAX_HEADING_LENGTH:
            continue
        folded = fold(stripped)
        for block, headings in BLOCK_HEADINGS.items():
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


def line_is_must(line: str, default_must: bool) -> bool:
    """Whether one line states a hard requirement.

    "Nice" is checked first on purpose. When a line carries both kinds of
    cue the softer reading is the safer error: a real must-have shown as
    preferred is a smaller problem for the reader than a preference shown
    as a blocking gap.
    """
    folded = fold(line)
    if any(fold(cue) in folded for cue in NICE_CUES):
        return False
    if any(fold(cue) in folded for cue in MUST_CUES):
        return True
    return default_must


BLOCK_DEFAULT_MUST = {"profile": True, "tasks": False, "intro": False}
SCANNED_BLOCKS = ("profile", "tasks", "intro")
"""The offer block is never scanned. Everything in it is what the employer
gives, not what the candidate needs."""


def parse_vacancy(text: str) -> VacancyProfile:
    blocks = split_blocks(text)
    scanned = {name: body for name, body in blocks.items() if name in SCANNED_BLOCKS}
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
            must = line_is_must(line, default_must)
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
            years = find_required_years(line)
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

    _add_education(scanned, text, add)
    _add_languages(scanned, add)

    licence = find_licence(text)
    if licence:
        add(
            Requirement(
                kind="licence",
                key=licence,
                label=f"Führerschein / licence {licence}",
                must=_licence_is_must(text),
                evidence=_line_containing(text, "hrerschein") or _line_containing(text, "licence") or "",
            )
        )

    ordered = sorted(
        requirements.values(),
        key=lambda r: (not r.must, KIND_ORDER.get(r.kind, 9), r.label.lower()),
    )
    return VacancyProfile(tuple(ordered), blocks)


KIND_ORDER = {"education": 0, "experience": 1, "language": 2, "licence": 3, "skill": 4}


def _add_education(scanned: dict[str, str], whole_text: str, add) -> None:
    if education_waived(whole_text):
        return
    best: Requirement | None = None
    for name, body in scanned.items():
        default_must = BLOCK_DEFAULT_MUST.get(name, False)
        for line in body.splitlines():
            fact = find_education(line)
            if fact is None:
                continue
            candidate = Requirement(
                kind="education",
                key=fact.level,
                label=_education_label(fact.level),
                must=line_is_must(line, default_must) and not fact.equivalent_accepted,
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


def _add_languages(scanned: dict[str, str], add) -> None:
    body = "\n".join(scanned.values())
    if not body.strip():
        return

    for fact in find_languages(body):
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

    for code in language_required_without_level(body):
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


def _licence_is_must(text: str) -> bool:
    line = _line_containing(text, "hrerschein") or _line_containing(text, "licence")
    return line_is_must(line, True) if line else True


def _line_containing(text: str, needle: str) -> str | None:
    lowered = needle.lower()
    for line in text.splitlines():
        if lowered in line.lower():
            return line.strip()
    return None
