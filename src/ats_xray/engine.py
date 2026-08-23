"""Rule engine: evaluates the registered rules and returns which ones
triggered, with evidence from the actual file.

``evaluate()`` is a pure function over already-computed signals (structure
findings + field reports), so it can be unit-tested with plain mock dicts
with no real PDF/DOCX files involved. ``run_rules()`` is the file-based
convenience wrapper the CLI uses: it gathers those signals from a real
file and calls ``evaluate()``.
"""

from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Callable

from . import rules as _rules  # noqa: F401  (import registers the rule set)
from .field_report import build_field_report
from .i18n import DEFAULT_LANGUAGE, t
from .regions import Region
from .rule import Rule, get_rule
from .structure import analyze_structure


@dataclass(frozen=True)
class Finding:
    rule: Rule
    evidence_key: str
    evidence_params: dict = field(default_factory=dict)
    regions: tuple[Region, ...] = ()
    """Where on the page the problem is, when that is knowable. Empty for
    DOCX (no page geometry) and for findings about something being absent,
    which by definition has no location."""
    severity_override: str | None = None
    """Set when *this instance* is more or less serious than the rule in
    general. A repeated footer holding a phone number risks losing contact
    details; the same rule firing on "Page 1 of 2" risks nothing. Reporting
    both at one level makes the level meaningless."""

    @property
    def severity(self) -> str:
        return self.severity_override or self.rule.severity

    @property
    def evidence(self) -> str:
        """The evidence rendered in English, for the CLI and for logs.
        The UI renders ``evidence_key`` in the reader's language instead."""
        return t(self.evidence_key, DEFAULT_LANGUAGE, **self.evidence_params)


Trigger = Callable[..., None]
"""A callback of (rule_id, evidence, regions=()) -> None, used by the
_evaluate_* helpers to record a triggered finding without each of them
needing to know how findings are collected.
"""


def evaluate(file_type: str, structure: dict, aware_fields: dict, naive_fields: dict) -> list[Finding]:
    """Evaluate every registered rule against pre-computed signals.

    ``file_type`` is ``"pdf"`` or ``"docx"``. ``structure`` is the dict
    shape returned by ``analyze_structure()`` for that file type.
    ``aware_fields``/``naive_fields`` are ``build_field_report()`` results
    for the layout-aware and naive extractions respectively.
    """
    findings: list[Finding] = []

    def trigger(
        rule_id: str,
        evidence_key: str,
        params: dict | None = None,
        regions: tuple = (),
        severity: str | None = None,
    ) -> None:
        findings.append(
            Finding(
                rule=get_rule(rule_id),
                evidence_key=evidence_key,
                evidence_params=params or {},
                regions=tuple(regions),
                severity_override=severity,
            )
        )

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
        trigger("pdf_non_embedded_font", "evidence_fonts", {"fonts": ", ".join(fonts)})

    repeated = structure.get("repeated_header_footer_lines") or []
    if repeated:
        sample = repeated[0]
        carries_contact = any(_holds_contact_details(entry["text"]) for entry in repeated)
        trigger(
            "pdf_repeated_header_footer_content",
            "evidence_repeated_line",
            {
                "zone": sample["zone"],
                "text": sample["text"],
                "pages": ", ".join(str(p) for p in sample["pages"]),
            },
            tuple(r for entry in repeated for r in entry.get("regions", ())),
            # Losing a running "Page 1 of 2" costs nothing; losing a running
            # footer that holds the phone number costs the application.
            severity="high" if carries_contact else "low",
        )

    images = structure.get("textless_images") or []
    if images:
        sample = images[0]
        trigger(
            "pdf_textless_image",
            "evidence_textless_image",
            {"page": sample["page"], "percent": f"{sample['area_fraction'] * 100:.0f}"},
            tuple(entry["region"] for entry in images if entry.get("region")),
            severity="high" if any(_is_banner_shaped(e) for e in images) else "low",
        )


def _evaluate_docx_structure(structure: dict, trigger: Trigger) -> None:
    headers_footers = structure.get("headers_footers") or {"headers": [], "footers": []}
    evidence_parts = headers_footers["headers"] + headers_footers["footers"]
    if evidence_parts:
        joined = "; ".join(evidence_parts)
        trigger(
            "docx_header_footer_content",
            "evidence_verbatim",
            {"text": joined},
            severity="high" if _holds_contact_details(joined) else "medium",
        )

    text_boxes = structure.get("text_box_content") or []
    if text_boxes:
        trigger("docx_text_box_content", "evidence_verbatim", {"text": "; ".join(text_boxes)})

    if structure.get("has_table_content"):
        trigger("docx_table_content", "evidence_table_cells")


BANNER_ASPECT_RATIO = 2.0
"""Width-to-height above which a textless image is treated as a banner --
a name plate or chart exported as a picture, whose text is genuinely lost.
Portrait or roughly square images are usually a profile photo, which is
normal on CVs in much of Europe and loses no text, so they are reported at
the lowest level rather than as a defect."""


def _is_banner_shaped(image: dict) -> bool:
    region = image.get("region")
    if region is None:
        return True  # no geometry to judge by; assume the worse case
    height = region.bottom - region.top
    if height <= 0:
        return True
    return (region.x1 - region.x0) / height >= BANNER_ASPECT_RATIO


def _holds_contact_details(text: str) -> bool:
    """True when the text carries an email or phone number, i.e. something
    whose loss would leave the candidate unreachable."""
    from .contact import find_email, find_phone

    return bool(find_email(text) or find_phone(text))


def _evaluate_fields(aware_fields: dict, naive_fields: dict, trigger: Trigger) -> None:
    if not aware_fields["email"]["found"] and not aware_fields["phone"]["found"]:
        trigger("missing_contact_field", "evidence_no_contact")

    at_risk = [
        section
        for section, aware_field in aware_fields["sections"].items()
        if aware_field["found"] and not naive_fields["sections"][section]["found"]
    ]
    if at_risk:
        listed = ", ".join(f'"{section}"' for section in at_risk)
        trigger(
            "section_missing_under_naive_parsing",
            "evidence_sections_lost_one" if len(at_risk) == 1 else "evidence_sections_lost_many",
            {"sections": listed},
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

    findings = evaluate(file_type, structure, aware_fields, naive_fields)

    if file_type == "pdf":
        findings = _attach_pdf_regions(file_path, findings, structure, aware_fields, naive_fields)

    return findings


def _attach_pdf_regions(
    file_path: str,
    findings: list[Finding],
    structure: dict,
    aware_fields: dict,
    naive_fields: dict,
) -> list[Finding]:
    """Fill in regions for findings whose location can only be resolved by
    going back to the PDF.

    Structural detectors already report coordinates as they scan, but two
    rules are decided by comparing extracted *text*, which has no geometry
    by the time the comparison happens — so their location is looked up here
    instead.
    """
    from .pdf_fonts import find_font_regions
    from .pdf_locate import find_section_regions
    from .sections import SECTION_ALIASES

    at_risk_sections = [
        section
        for section, aware in aware_fields["sections"].items()
        if aware["found"] and not naive_fields["sections"][section]["found"]
    ]

    enriched: list[Finding] = []
    for finding in findings:
        if finding.regions:
            enriched.append(finding)
            continue

        if finding.rule.id == "pdf_non_embedded_font":
            regions = find_font_regions(file_path, structure.get("non_embedded_fonts") or [])
            enriched.append(replace(finding, regions=tuple(regions)))
        elif finding.rule.id == "section_missing_under_naive_parsing" and at_risk_sections:
            aliases = {alias for section in at_risk_sections for alias in SECTION_ALIASES[section]}
            regions = find_section_regions(file_path, aliases)
            enriched.append(replace(finding, regions=tuple(regions)))
        else:
            enriched.append(finding)

    return enriched


def attach_docx_regions(
    rendered_pdf_path: str,
    findings: list[Finding],
    structure: dict,
    aware_fields: dict,
    naive_fields: dict,
) -> list[Finding]:
    """Place DOCX findings on a laid-out rendering of the same document.

    DOCX detectors work on XML, which carries no positions, so findings
    arrive with no regions. Once the document has been through a layout
    engine we have a page to point at, and the only route from a finding
    back to a position is the text it reported: search the rendered page
    for that text.

    ``rendered_pdf_path`` must be a rendering of the same DOCX the findings
    came from. Content the layout engine places off-page, or drops, simply
    yields no region -- the finding still stands on its text evidence.
    """
    from .pdf_locate import find_section_regions, find_text_regions
    from .sections import SECTION_ALIASES

    headers_footers = structure.get("headers_footers") or {"headers": [], "footers": []}
    texts_by_rule = {
        "docx_header_footer_content": headers_footers["headers"] + headers_footers["footers"],
        "docx_text_box_content": structure.get("text_box_content") or [],
        "docx_table_content": structure.get("table_texts") or [],
    }

    at_risk_sections = [
        section
        for section, aware in aware_fields["sections"].items()
        if aware["found"] and not naive_fields["sections"][section]["found"]
    ]

    enriched: list[Finding] = []
    for finding in findings:
        if finding.regions:
            enriched.append(finding)
        elif finding.rule.id in texts_by_rule:
            regions = find_text_regions(rendered_pdf_path, texts_by_rule[finding.rule.id])
            enriched.append(replace(finding, regions=tuple(regions)))
        elif finding.rule.id == "section_missing_under_naive_parsing" and at_risk_sections:
            aliases = {alias for section in at_risk_sections for alias in SECTION_ALIASES[section]}
            regions = find_section_regions(rendered_pdf_path, aliases)
            enriched.append(replace(finding, regions=tuple(regions)))
        else:
            enriched.append(finding)

    return enriched
