"""The registered rules: documented resume-parsing risks that the detectors
in ``structure.py`` and ``field_report.py`` can find evidence for, and the
national CV conventions that ``conventions.py`` checks. See
``research_sources.md`` for the citation behind each ``source`` key.

Evaluating these rules against an actual file is a separate concern, handled
by ``engine.py``, so the claims made here can be reviewed on their own,
independent of the code that checks for them.
"""

from .rule import CONVENTION, Rule, register

NON_EMBEDDED_FONT = register(
    Rule(
        id="pdf_non_embedded_font",
        description=(
            "A font used in the PDF is not embedded and is not one of the 14 "
            "standard PDF base fonts. Non-embedded, non-standard fonts risk "
            "character-mapping issues that cause garbled or missing text "
            "during parsing."
        ),
        severity="medium",
        source="ats-fonts",
    )
)

REPEATED_HEADER_FOOTER_CONTENT = register(
    Rule(
        id="pdf_repeated_header_footer_content",
        description=(
            "Text repeats in the same header/footer zone across multiple PDF "
            "pages. Parsers commonly treat repeated header/footer content as "
            "boilerplate and strip it — a problem if essential info (phone, "
            "email) lives there."
        ),
        severity="medium",
        source="ats-headers-footers",
    )
)

TEXTLESS_IMAGE = register(
    Rule(
        id="pdf_textless_image",
        description=(
            "A large image on the page has no extracted text overlapping it "
            "— a sign that a name banner, skills chart, or whole section may "
            "have been exported as a picture instead of real text, which "
            "most parsers cannot read at all."
        ),
        severity="high",
        source="ats-graphics",
    )
)

DOCX_TABLE_CONTENT = register(
    Rule(
        id="docx_table_content",
        description=(
            "Resume content lives inside a DOCX table. Many parsers flatten "
            "table rows in a way that scrambles which value belongs to which "
            "label, or skip table content entirely."
        ),
        severity="high",
        source="ats-tables-columns",
    )
)

DOCX_HEADER_FOOTER_CONTENT = register(
    Rule(
        id="docx_header_footer_content",
        description=(
            "Resume content (often contact info) lives in a DOCX header or "
            "footer — a part of the file that lives outside the main "
            "document body and that many parsers skip entirely."
        ),
        severity="high",
        source="ats-headers-footers",
    )
)

DOCX_TEXT_BOX_CONTENT = register(
    Rule(
        id="docx_text_box_content",
        description=(
            "Resume content lives inside a Word text box, nested inside a "
            "drawing anchor rather than the normal paragraph flow most "
            "parsers read."
        ),
        severity="high",
        source="ats-text-boxes",
    )
)

MISSING_CONTACT_FIELD = register(
    Rule(
        id="missing_contact_field",
        description=(
            "No email address and/or phone number could be found anywhere "
            "in the extracted text, even reading layout-aware, best case. "
            "Without a way to reach the candidate, this is typically an "
            "unrecoverable rejection regardless of formatting."
        ),
        severity="high",
        source="practical-necessity",
    )
)

SECTION_MISSING_UNDER_NAIVE_PARSING = register(
    Rule(
        id="section_missing_under_naive_parsing",
        description=(
            "A resume section (Experience/Education/Skills) is recognized "
            "when the file is read layout-aware, but disappears entirely "
            "when read the way a naive, layout-blind parser would — "
            "evidence that formatting, not content, is putting this section "
            "at risk."
        ),
        severity="high",
        source="ats-tables-columns",
    )
)

CONTACT_ONLY_AS_LINK = register(
    Rule(
        id="contact_only_as_link",
        description=(
            "The only route to the candidate is a hyperlink — a LinkedIn or "
            "portfolio profile, or a mailto: — with no email address or "
            "phone number written out as text. The link text is what a "
            "parser reads; the address behind it lives in an annotation "
            "most extractors never open."
        ),
        severity="high",
        source="practical-necessity",
    )
)

UNRECOGNISED_SECTION_HEADINGS = register(
    Rule(
        id="unrecognised_section_headings",
        description=(
            "The document is organised under headings, but none of them is "
            "a heading a parser recognises. Software finds Experience and "
            "Education by their names; under invented labels the content is "
            "read as one undifferentiated block, and no history can be "
            "mapped to a role or a date."
        ),
        severity="high",
        source="ats-tables-columns",
    )
)

BROKEN_CHARACTERS = register(
    Rule(
        id="broken_characters",
        description=(
            "A word contains characters that are not the letters they look "
            "like: a typographic ligature, an invisible soft hyphen or "
            "zero-width space, or a mix of Latin and Cyrillic. The word "
            "reads normally on screen and matches nothing a recruiter "
            "searches for."
        ),
        severity="medium",
        source="ats-fonts",
    )
)


# --------------------------------------------------------------------------
# Conventions: the file reads fine, and says something a recruiter in that
# country does not expect. Detected in ``conventions.py``; never scored.
# --------------------------------------------------------------------------

VOLUNTEERING_LISTED_AS_EMPLOYMENT = register(
    Rule(
        id="volunteering_listed_as_employment",
        description=(
            "Volunteer work is listed under work experience. In a German or "
            "Ukrainian CV that section means paid employment, so a recruiter "
            "reads the entry as a job and then finds out it was not one."
        ),
        severity="medium",
        source="cv-volunteering",
        category=CONVENTION,
    )
)

UNEXPLAINED_GAP = register(
    Rule(
        id="unexplained_gap",
        description=(
            "The dates leave months with nothing in them. German recruiters "
            "expect a CV without unexplained gaps, and read a silent one as "
            "something being left out."
        ),
        severity="medium",
        source="cv-gaps",
        category=CONVENTION,
    )
)

IMPOSSIBLE_DATES = register(
    Rule(
        id="impossible_dates",
        description=(
            "A date range cannot be true: it ends before it starts, or it "
            "reaches years into the future. Software that works out years of "
            "experience from the dates discards the range entirely."
        ),
        severity="medium",
        source="cv-date-logic",
        category=CONVENTION,
    )
)

FIRST_PERSON_IN_CV = register(
    Rule(
        id="first_person_in_cv",
        description=(
            "Entries are written as sentences about \"I\". A CV lists its "
            "entries as short fragments; first-person sentences belong in the "
            "profile at the top or in the cover letter."
        ),
        severity="low",
        source="cv-first-person",
        category=CONVENTION,
    )
)

OUTDATED_PERSONAL_DETAILS = register(
    Rule(
        id="outdated_personal_details",
        description=(
            "The personal details include fields a German CV no longer needs: "
            "religion, marital status, children or parents. Religion is "
            "protected under the equal treatment law, and the rest are "
            "details most applicants no longer give."
        ),
        severity="low",
        source="cv-personal-details",
        category=CONVENTION,
    )
)

OLDEST_ENTRY_FIRST = register(
    Rule(
        id="oldest_entry_first",
        description=(
            "Work experience runs from the oldest job to the newest. The "
            "expected order is the reverse, so that the first thing a "
            "recruiter reads is what the candidate does now."
        ),
        severity="low",
        source="cv-reverse-chronological",
        category=CONVENTION,
    )
)
