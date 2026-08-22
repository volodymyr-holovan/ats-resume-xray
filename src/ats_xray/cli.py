"""Command-line entry point: ``atsxray path/to/resume.pdf``."""

import argparse
import sys
from pathlib import Path

from .engine import run_rules
from .field_report import build_field_report
from .pipeline import extract_text
from .score import score_resume
from .structure import analyze_structure

_SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}

SEPARATOR = "=" * 30


def main() -> None:
    # Resume content is arbitrary Unicode (umlauts, em-dashes, non-Latin
    # names); the OS console's default codepage often isn't UTF-8 and can't
    # represent it, which crashes print() with UnicodeEncodeError instead of
    # just looking wrong. Force UTF-8 stdout/stderr regardless of locale.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        prog="atsxray",
        description="Show what a resume-parsing pipeline actually extracts from your file.",
    )
    parser.add_argument("file", help="Path to a .pdf or .docx resume")
    parser.add_argument(
        "--structure",
        action="store_true",
        help="Also run structural analysis (fonts, headers/footers, images/text boxes)",
    )
    parser.add_argument(
        "--fields",
        action="store_true",
        help="Also run field recognition (name/email/phone/sections), comparing naive vs layout-aware extraction",
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Also run the rule engine and print triggered findings, each with its evidence and cited source",
    )
    parser.add_argument(
        "--score",
        action="store_true",
        help="Also print the parse readiness score with the arithmetic behind it",
    )
    args = parser.parse_args()

    path = Path(args.file)

    if not path.exists():
        raise SystemExit(f"File not found: {path}")

    try:
        naive, aware = extract_text(str(path))
    except ValueError as exc:
        raise SystemExit(str(exc))
    except Exception:
        raise SystemExit(
            f"Couldn't read {path} — it may be corrupted, password-protected, "
            "or not a valid PDF/DOCX."
        )

    print(SEPARATOR, "NAIVE EXTRACTION (what a basic parser sees)", SEPARATOR)
    print(naive)
    print()
    print(SEPARATOR, "LAYOUT-AWARE EXTRACTION (columns/tables handled)", SEPARATOR)
    print(aware)

    if args.structure:
        print()
        print(SEPARATOR, "STRUCTURAL ANALYSIS", SEPARATOR)
        print(_format_structure_report(analyze_structure(str(path))))

    if args.fields:
        print()
        print(SEPARATOR, "FIELD RECOGNITION (layout-aware vs. naive)", SEPARATOR)
        print(_format_field_comparison(build_field_report(aware), build_field_report(naive)))

    if args.report:
        print()
        print(SEPARATOR, "RULE ENGINE REPORT", SEPARATOR)
        print(_format_rule_report(run_rules(str(path), naive, aware)))

    if args.score:
        breakdown = score_resume(
            build_field_report(aware), build_field_report(naive), run_rules(str(path), naive, aware)
        )
        print()
        print(SEPARATOR, "PARSE READINESS", SEPARATOR)
        print(_format_score(breakdown))


def _format_score(breakdown) -> str:
    lines = [f"{breakdown.total}/100 - {breakdown.rating}"]
    if breakdown.cap_reason:
        lines.append(f"  {breakdown.cap_reason} (before the cap: {breakdown.uncapped_total}/100)")
    lines.append("")
    for component in breakdown.components:
        weight = "not scored" if component.weight == 0 else f"weight {component.weight}%"
        lines.append(f"  {component.name}: {component.score:.0f}/100 ({weight})")
        lines.append(f"    {component.detail}")
    lines.append("")
    lines.append("  Measures parse readiness only, not keyword match against a job posting.")
    return "\n".join(lines)


def _format_structure_report(findings: dict) -> str:
    lines: list[str] = []

    if "non_embedded_fonts" in findings:
        fonts = findings["non_embedded_fonts"]
        lines.append("Non-embedded, non-standard fonts: " + (", ".join(fonts) if fonts else "none found"))

        repeated = findings["repeated_header_footer_lines"]
        lines.append("Repeated header/footer lines:" if repeated else "Repeated header/footer lines: none found")
        for entry in repeated:
            pages = ", ".join(str(p) for p in entry["pages"])
            lines.append(f'  [{entry["zone"]}] "{entry["text"]}" (pages {pages})')

        images = findings["textless_images"]
        lines.append(
            "Large images with no extracted text:" if images else "Large images with no extracted text: none found"
        )
        for image in images:
            lines.append(
                f"  page {image['page']}, {image['area_fraction'] * 100:.0f}% of page area, bbox {image['bbox']}"
            )

    if "headers_footers" in findings:
        headers = findings["headers_footers"]["headers"]
        lines.append("Header content (invisible to naive extraction):" if headers else "Header content: none found")
        for header in headers:
            lines.append(f"  {header}")

        footers = findings["headers_footers"]["footers"]
        lines.append("Footer content (invisible to naive extraction):" if footers else "Footer content: none found")
        for footer in footers:
            lines.append(f"  {footer}")

        text_boxes = findings["text_box_content"]
        lines.append(
            "Text box content (invisible to naive AND full extraction):"
            if text_boxes
            else "Text box content: none found"
        )
        for text_box in text_boxes:
            lines.append(f"  {text_box}")

        lines.append(
            "Table content: found (many parsers scramble or skip table rows)"
            if findings.get("has_table_content")
            else "Table content: none found"
        )

    return "\n".join(lines)


def _format_field_comparison(aware_report: dict, naive_report: dict) -> str:
    lines: list[str] = []

    for field in ("name", "email", "phone"):
        lines.append(_comparison_line(field, aware_report[field], naive_report[field]))

    for section, aware_field in aware_report["sections"].items():
        lines.append(_comparison_line(section, aware_field, naive_report["sections"][section]))

    return "\n".join(lines)


def _comparison_line(label: str, aware_field: dict, naive_field: dict) -> str:
    aware_status = "found" if aware_field["found"] else "MISSING"
    naive_status = "found" if naive_field["found"] else "MISSING"
    line = f"{label}: layout-aware={aware_status}, naive={naive_status}"
    if aware_field["found"] and not naive_field["found"]:
        line += "  <-- at risk: a basic parser would miss this"
    return line


def _format_rule_report(findings: list) -> str:
    if not findings:
        return "No rules triggered."

    ordered = sorted(findings, key=lambda f: _SEVERITY_ORDER[f.rule.severity])
    blocks = []
    for finding in ordered:
        blocks.append(
            "\n".join(
                [
                    f"[{finding.rule.severity.upper()}] {finding.rule.id}",
                    f"  {finding.rule.description}",
                    f"  Evidence: {finding.evidence}",
                    f"  Source: research_sources.md#{finding.rule.source}",
                ]
            )
        )
    return "\n\n".join(blocks)


if __name__ == "__main__":
    main()
