"""The registered rules: documented resume-parsing risks that the detectors
in ``structure.py`` and ``field_report.py`` can find evidence for. See
``research_sources.md`` for the citation behind each ``source`` key.

Evaluating these rules against an actual file is a separate concern, handled
by ``engine.py``, so the claims made here can be reviewed on their own,
independent of the code that checks for them.
"""

from .rule import Rule, register

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
