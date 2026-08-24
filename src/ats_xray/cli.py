"""Command-line entry point: ``atsxray path/to/resume.pdf``."""

import argparse
import sys
import textwrap
from pathlib import Path

from .engine import run_rules
from .field_report import build_field_report
from .i18n import (
    DEFAULT_LANGUAGE,
    UI_LANGUAGES,
    rule_description,
    rule_detail,
    rule_fixes,
    sources_path,
    t,
    tn,
)
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
    parser.add_argument(
        "--language",
        default=DEFAULT_LANGUAGE,
        choices=sorted(UI_LANGUAGES),
        help="Language for findings, fixes and the score (default: %(default)s)",
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
        print(_format_rule_report(run_rules(str(path), naive, aware), args.language))

    if args.score:
        breakdown = score_resume(
            build_field_report(aware), build_field_report(naive), run_rules(str(path), naive, aware)
        )
        print()
        print(SEPARATOR, "PARSE READINESS", SEPARATOR)
        print(_format_score(breakdown, args.language))


def _format_score(breakdown, language: str = DEFAULT_LANGUAGE) -> str:
    lines = [f"{breakdown.total}/100 - {t(breakdown.rating_key, language)}"]
    if breakdown.cap_key:
        lines.append(f"  {tn(breakdown.cap_key, breakdown.cap_params.get("count", 1), language, **breakdown.cap_params)}")
    lines.append("")
    for component in breakdown.components:
        weight = (
            t("not_scored", language)
            if component.weight == 0
            else f"{t('weight', language)} {component.weight}%"
        )
        lines.append(f"  {t(component.name_key, language)}: {component.score:.0f}/100 ({weight})")
        lines.append(f"    {t(component.detail_key, language, **component.detail_params)}")
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


def _format_rule_report(findings: list, language: str = DEFAULT_LANGUAGE) -> str:
    if not findings:
        return t("no_findings", language)

    ordered = sorted(findings, key=lambda f: _SEVERITY_ORDER[f.severity])
    return "\n\n".join(_format_finding(finding, language) for finding in ordered)


def _format_finding(finding, language: str) -> str:
    """One finding at full depth: what fired, what it means, what to do about
    it. The web UI folds the last two behind an expander because it can; a
    terminal has no fold, so it prints the lot."""
    lines = [
        f"[{t('severity_' + finding.severity, language)}] {finding.rule.id}",
        f"  {rule_description(finding.rule.id, language, finding.rule.description)}",
    ]

    detail = rule_detail(finding.rule.id, language)
    if detail:
        lines.extend(f"  {line}" for line in textwrap.wrap(detail, width=78))

    fixes = rule_fixes(finding.rule.id, language)
    if fixes:
        lines.append(f"  {t('how_to_fix', language)}:")
        for number, fix in enumerate(fixes, 1):
            wrapped = textwrap.wrap(fix, width=74) or [""]
            lines.append(f"    {number}. {wrapped[0]}")
            lines.extend(f"       {line}" for line in wrapped[1:])

    evidence = t(finding.evidence_key, language, **finding.evidence_params)
    lines.append(f"  {t('evidence', language)}: {evidence}")
    lines.append(f"  {t('source', language)}: {sources_path(language)}#{finding.rule.source}")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
