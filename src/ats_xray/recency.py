"""When a skill was last actually used.

A CV lists what someone can do; it rarely says when they last did it. The
dates are there, but attached to the job rather than to the skill, so a
keyword match treats "Photoshop, 2011-2013" and "Photoshop, still doing it"
as the same fact. An employer does not.

This walks the dated entries of a CV and works out, for each entry, when it
ended — so a matched skill can be told apart into one that is current and
one that has not been touched in a decade. Nothing here guesses: a skill
with no date attached is treated as current, because a Skills section is a
statement about now.
"""

from dataclasses import dataclass
from datetime import date

from .credentials import range_end
from .sections import split_into_sections
from .skills_lexicon import find_skills

STALE_AFTER_YEARS = 6
"""How long since an entry ended before the skills in it are worth a
mention.

Long enough not to nag: a five-year-old project is recent history in most
careers, and tools that mature slowly -- a language, a trade, a
certification -- do not go stale on any schedule an algorithm can know. Six
years is roughly the point at which "when did you last use this?" becomes a
fair question in an interview, which is the moment worth warning about."""


@dataclass(frozen=True)
class Entry:
    """One dated block of a CV: a job, a project, a course."""

    text: str
    ended: int
    """Month index since year zero, or 0 for an entry that has not ended."""

    @property
    def is_current(self) -> bool:
        return self.ended == 0


def find_dated_entries(text: str, today: date | None = None) -> list[Entry]:
    """Split text into the blocks its date ranges introduce.

    A CV entry starts with a date and runs until the next one. That is a
    convention rather than a rule, which is why nothing downstream treats
    the absence of an entry as meaningful.
    """
    today = today or date.today()
    lines = text.splitlines()
    starts: list[tuple[int, int]] = []

    for index, line in enumerate(lines):
        ended = range_end(line, today)
        if ended is not None:
            starts.append((index, ended))

    entries = []
    for position, (index, ended) in enumerate(starts):
        stop = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        body = "\n".join(lines[index:stop]).strip()
        if body:
            entries.append(Entry(text=body, ended=ended))
    return entries


def last_used(skill_id: str, entries: list[Entry]) -> int | None:
    """The month index when this skill was last in a dated entry.

    ``0`` means an entry that is still running. ``None`` means the skill
    appears in no dated entry at all -- which is the ordinary case for a
    Skills section and is not a finding.
    """
    seen = [entry.ended for entry in entries if skill_id in find_skills(entry.text)]
    if not seen:
        return None
    if 0 in seen:
        return 0
    return max(seen)


def is_stale(skill_id: str, text: str, entries: list[Entry], today: date | None = None) -> bool:
    """Whether every dated mention of this skill is old enough to ask about.

    A skill named in the Skills section is never stale, whatever the dated
    entries say: listing it is a claim about the present, and calling that
    out would be arguing with the candidate about their own CV.
    """
    sections = split_into_sections(text)
    listed = sections.get("skills")
    if listed and skill_id in find_skills(listed):
        return False

    ended = last_used(skill_id, entries)
    if ended is None or ended == 0:
        return False

    today = today or date.today()
    months_ago = (today.year * 12 + today.month) - ended
    return months_ago > STALE_AFTER_YEARS * 12


def years_since(ended: int, today: date | None = None) -> int:
    """Whole years between an entry's end and now, for saying it out loud."""
    today = today or date.today()
    return max(0, ((today.year * 12 + today.month) - ended) // 12)
