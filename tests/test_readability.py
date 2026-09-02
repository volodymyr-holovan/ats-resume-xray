"""Faults in the recovered text, which no file format can be asked about.

Each of these three is a real shape of CV, and each looks correct to the
person who wrote it. That is what makes them worth a finding: nothing on
the page tells the author anything is wrong.
"""

import pytest

from ats_xray.readability import (
    find_broken_characters,
    find_link_only_contact,
    find_unrecognised_headings,
)

# --------------------------------------------------------------------------
# Contact only behind a link
# --------------------------------------------------------------------------

LINK_ONLY = """Anna Muster
Grafikdesignerin, Hamburg
LinkedIn: linkedin.com/in/annamuster
Portfolio: behance.net/annamuster"""


def test_a_profile_link_with_no_written_address_is_reported():
    assert "linkedin.com" in find_link_only_contact(LINK_ONLY)


def test_a_mailto_with_no_written_address_is_reported():
    assert "mailto:" in find_link_only_contact("Anna Muster\nmailto:anna@")


@pytest.mark.parametrize(
    "text",
    [
        "Anna Muster\nanna@example.com\n040 1234567\nlinkedin.com/in/annamuster",
        "Anna Muster\nanna@example.com\nlinkedin.com/in/annamuster",
        "Anna Muster\n+49 170 1234567\nlinkedin.com/in/annamuster",
    ],
)
def test_a_link_beside_a_written_address_is_not_a_finding(text):
    """The link is not the problem; being the only route is. A CV that has
    both is doing the right thing and must not be told off for it."""
    assert find_link_only_contact(text) == []


def test_a_cv_with_no_links_at_all_is_not_a_finding():
    """That case is already `missing_contact_field`, and saying it twice
    would make the report look longer than the problem."""
    assert find_link_only_contact("Anna Muster\nHamburg") == []


# --------------------------------------------------------------------------
# Headings a parser cannot place
# --------------------------------------------------------------------------

CREATIVE = """Anna Muster
anna@example.com

My Journey
Studio Nord, Hamburg
Designer

What I Bring
InDesign, Photoshop

Where I Studied
HAW Hamburg"""

CONVENTIONAL = """Anna Muster
anna@example.com

Experience
Studio Nord, Hamburg

Education
HAW Hamburg"""


def test_invented_headings_are_reported():
    found = find_unrecognised_headings(CREATIVE)

    assert found == ["My Journey", "What I Bring", "Where I Studied"]


def test_recognised_headings_silence_the_rule_entirely():
    """One anchor is enough. A CV with "Experience" and one creative
    heading is readable, and warning about the creative one would be
    noise."""
    assert find_unrecognised_headings(CONVENTIONAL) == []


def test_the_name_at_the_top_is_not_a_heading():
    """A looser version of this test reported the candidate's own name and
    their job title as unrecognised headings -- a finding worse than
    none."""
    found = find_unrecognised_headings(CREATIVE)

    assert "Anna Muster" not in found


def test_content_lines_are_not_headings():
    for line in ("Studio Nord, Hamburg", "InDesign, Photoshop", "Designer"):
        assert line not in find_unrecognised_headings(CREATIVE)


def test_a_single_heading_shaped_line_is_not_enough():
    """One is far more likely to be a job title than a section label."""
    text = "Anna Muster\nanna@example.com\n\nSenior Designer\nStudio Nord und weitere Projekte"

    assert find_unrecognised_headings(text) == []


def test_headings_are_found_in_other_languages_too():
    """The rule is about the absence of known words, so it works wherever
    the reader writes -- there is nothing language-specific to get right."""
    german = "Anna Muster\nanna@example.com\n\nWas ich mitbringe\nInDesign\n\nWo ich war\nStudio Nord"

    assert find_unrecognised_headings(german) == ["Was ich mitbringe", "Wo ich war"]


# --------------------------------------------------------------------------
# Characters that are not the letters they look like
# --------------------------------------------------------------------------


def test_a_ligature_is_reported_with_the_letters_it_stands_for():
    found = find_broken_characters("Proﬁl: Grafikdesign")

    assert found and "fi" in found[0]


@pytest.mark.parametrize(
    "character,name",
    [("­", "soft hyphen"), ("​", "zero-width space"), ("﻿", "byte-order mark")],
)
def test_an_invisible_character_is_reported(character, name):
    assert name in find_broken_characters(f"Grafik{character}design")


def test_a_word_mixing_alphabets_is_reported():
    """The project shipped this bug itself: an alias in the skill list held
    a Cyrillic o and could never match Latin text. One character, invisible
    to review, and no test could see it."""
    found = find_broken_characters("RenоFachangestellte")

    assert found and "Cyrillic" in found[0]


@pytest.mark.parametrize(
    "text",
    [
        "Grafikdesign und Reinzeichnung",
        "Розробка та підтримка",
        "Anna Muster — Designer",
        "naive-parsing",
    ],
)
def test_ordinary_text_is_left_alone(text):
    """Including a Cyrillic-only line and an em dash, neither of which is a
    mixed word."""
    assert find_broken_characters(text) == []


PDF_SHAPED = """Maria Weber
Pflegefachkraft
LinkedIn: linkedin.com/in/mariaweber
Mein Weg
Marz 2019 - heute Seniorenheim Nordlicht
Grundpflege und Behandlungspflege
Was ich gelernt habe
September 2008 - August 2011 Pflegeschule Bremen"""


def test_headings_are_found_without_blank_lines():
    """The shape a PDF actually arrives in. pdfplumber returns the lines it
    finds and not the space between them, so the blank-line signal this
    rule was first written around is absent from the majority format --
    which meant the rule fired on DOCX files and quietly never on PDFs.

    A heading whose next line opens a dated entry is the signal that
    survives."""
    assert find_unrecognised_headings(PDF_SHAPED) == ["Mein Weg", "Was ich gelernt habe"]


def test_a_job_title_above_a_date_is_not_a_heading():
    """The cost of that second signal: a job title sitting under the name
    and above a date looks exactly like a section label. The first two
    lines are excluded, and needing two headings does the rest."""
    text = "Anna Muster\nanna@example.com\nSenior Designer\n03/2019 - heute Studio Nord\nGestaltung"

    assert find_unrecognised_headings(text) == []
