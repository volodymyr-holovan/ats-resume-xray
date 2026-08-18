"""Expected rule-engine output for each fixture in golden_generators.py:
the exact set of rule ids that must trigger — no more, no less. A fixture
mapping to an empty set is a clean-resume control.

Kept as data separate from the test harness so the expected behavior is
readable and reviewable on its own, independent of how it gets asserted.
"""

import golden_generators as generators

GOLDEN_CASES: dict = {
    generators.clean_single_column: set(),
    generators.two_column_pdf: {"section_missing_under_naive_parsing"},
    generators.missing_contact: {"missing_contact_field"},
    generators.pdf_textless_image: {"pdf_textless_image"},
    generators.pdf_repeated_header_footer: {"pdf_repeated_header_footer_content"},
    generators.docx_with_table: {"docx_table_content"},
    generators.docx_contact_in_header: {"docx_header_footer_content", "missing_contact_field"},
    generators.docx_text_box: {"docx_text_box_content"},
}
