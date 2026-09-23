"""Expected rule-engine output for each fixture in golden_generators.py:
its file suffix (which format to generate it as) and the exact set of
rule ids that must trigger — no more, no less. A fixture mapping to an
empty set is a clean-resume control.

Kept as data separate from the test harness so the expected behavior is
readable and reviewable on its own, independent of how it gets asserted.
"""

import golden_generators as generators

# (generator, file suffix, expected rule ids)
GOLDEN_CASES: list[tuple] = [
    (generators.clean_single_column, ".pdf", set()),
    (generators.missing_optional_section, ".pdf", set()),
    (generators.contact_with_only_email, ".pdf", set()),
    (generators.two_column_pdf, ".pdf", {"section_missing_under_naive_parsing"}),
    (generators.missing_contact, ".pdf", {"missing_contact_field"}),
    (generators.pdf_textless_image, ".pdf", {"pdf_textless_image"}),
    (generators.pdf_repeated_header_footer, ".pdf", {"pdf_repeated_header_footer_content"}),
    (generators.pdf_unembedded_font, ".pdf", {"pdf_non_embedded_font"}),
    (generators.pdf_contact_only_as_link, ".pdf",
     {"contact_only_as_link", "missing_contact_field"}),
    (generators.pdf_invented_headings, ".pdf", {"unrecognised_section_headings"}),
    (generators.pdf_broken_characters, ".pdf", {"broken_characters"}),
    (generators.docx_with_table, ".docx", {"docx_table_content"}),
    (generators.docx_contact_in_header, ".docx", {"docx_header_footer_content", "missing_contact_field"}),
    (generators.docx_text_box, ".docx", {"docx_text_box_content"}),
]
