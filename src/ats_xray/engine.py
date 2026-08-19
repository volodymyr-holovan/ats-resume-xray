"""Rule engine: evaluates the registered rules and returns which ones
triggered, with evidence from the actual file.

``evaluate()`` is a pure function over already-computed signals (structure
findings + field reports), so it can be unit-tested with plain mock dicts
with no real PDF/DOCX files involved. ``run_rules()`` is the file-based
convenience wrapper the CLI uses: it gathers those signals from a real
file and calls ``evaluate()``.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from . import rules as _rules  # noqa: F401  (import registers the rule set)
from .field_report import build_field_report
from .rule import Rule, get_rule
from .structure import analyze_structure


@dataclass(frozen=True)
class Finding:
    rule: Rule
    evidence: str


Trigger = Callable[[str, str], None]
"""A callback of (rule_id, evidence) -> None, used by the _evaluate_* helpers
to record a triggered finding without each of them needing to know how
findings are collected.
"""


def evaluate(file_type: str, structure: dict, aware_fields: dict, naive_fields: dict) -> list[Finding]:
    """Evaluate every registered rule against pre-computed signals.

    ``file_type`` is ``"pdf"`` or ``"docx"``. ``structure`` is the dict
    shape returned by ``analyze_structure()`` for that file type.
    ``aware_fields``/``naive_fields`` are ``build_field_report()`` results
    for the layout-aware and naive extractions respectively.
    """
    findings: list[Finding] = []

    def trigger(rule_id: str, evidence: str) -> None:
        findings.append(Finding(rule=get_rule(rule_id), evidence=evidence))

    if file_type == "pdf":
        _evaluate_pdf_structure(structure, trigger)
    elif file_type == "docx":
        _evaluate_docx_structure(structure, trigger)
    else:
        raise ValueError(f"Unknown file_type: {file_type!r}, expected 'pdf' or 'docx'")

    _evaluate_fields(aware_fields, naive_fields, trigger)

    return findings


def _evaluate_pdf_structure(structure: dict, trigger: Trigger) -> None:
    fonts = structure.get("non_embedded_fonts") or []
    if fonts:
        trigger("pdf_non_embedded_font", f"Non-embedded fonts: {', '.join(fonts)}")

    repeated = structure.get("repeated_header_footer_lines") or []
    if repeated:
        sample = repeated[0]
        trigger(
            "pdf_repeated_header_footer_content",
            f'[{sample["zone"]}] "{sample["text"]}" on pages {sample["pages"]}',
        )

    images = structure.get("textless_images") or []
    if images:
        sample = images[0]
        trigger(
            "pdf_textless_image",
            f"page {sample['page']}, {sample['area_fraction'] * 100:.0f}% of page area",
        )


def _evaluate_docx_structure(structure: dict, trigger: Trigger) -> None:
    headers_footers = structure.get("headers_footers") or {"headers": [], "footers": []}
    evidence_parts = headers_footers["headers"] + headers_footers["footers"]
    if evidence_parts:
        trigger("docx_header_footer_content", "; ".join(evidence_parts))

    text_boxes = structure.get("text_box_content") or []
    if text_boxes:
        trigger("docx_text_box_content", "; ".join(text_boxes))

    if structure.get("has_table_content"):
        trigger("docx_table_content", "One or more table cells contain resume content")


def _evaluate_fields(aware_fields: dict, naive_fields: dict, trigger: Trigger) -> None:
    if not aware_fields["email"]["found"] and not aware_fields["phone"]["found"]:
        trigger("missing_contact_field", "No email or phone found anywhere in the extracted text")

    for section, aware_field in aware_fields["sections"].items():
        naive_field = naive_fields["sections"][section]
        if aware_field["found"] and not naive_field["found"]:
            trigger(
                "section_missing_under_naive_parsing",
                f'"{section}" section found layout-aware but missing under naive parsing',
            )


def run_rules(file_path: str, naive_text: str, aware_text: str) -> list[Finding]:
    """Gather signals from a real file and evaluate the rule set against
    them. ``naive_text``/``aware_text`` are the extractions the caller
    already computed, passed in rather than recomputed here.
    """
    suffix = Path(file_path).suffix.lower()
    if suffix == ".pdf":
        file_type = "pdf"
    elif suffix == ".docx":
        file_type = "docx"
    else:
        raise ValueError(f"Unsupported file type: {suffix or '(none)'}. Use .pdf or .docx.")

    structure = analyze_structure(file_path)
    aware_fields = build_field_report(aware_text)
    naive_fields = build_field_report(naive_text)

    return evaluate(file_type, structure, aware_fields, naive_fields)
