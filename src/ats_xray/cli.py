"""Command-line entry point: ``atsxray path/to/resume.pdf``."""

import argparse
from pathlib import Path

from .docx_extract import extract_docx_full, extract_docx_naive
from .extract import extract_layout_aware, extract_naive
from .structure import analyze_structure

SEPARATOR = "=" * 30


def main() -> None:
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
    args = parser.parse_args()

    path = Path(args.file)
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        naive = extract_naive(str(path))
        aware = extract_layout_aware(str(path))
    elif suffix == ".docx":
        naive = extract_docx_naive(str(path))
        aware = extract_docx_full(str(path))
    else:
        raise SystemExit(f"Unsupported file type: {suffix or '(none)'}. Use .pdf or .docx.")

    print(SEPARATOR, "NAIVE EXTRACTION (what a basic parser sees)", SEPARATOR)
    print(naive)
    print()
    print(SEPARATOR, "LAYOUT-AWARE EXTRACTION (columns/tables handled)", SEPARATOR)
    print(aware)

    if args.structure:
        print()
        print(SEPARATOR, "STRUCTURAL ANALYSIS", SEPARATOR)
        print(_format_structure_report(analyze_structure(str(path))))


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

    return "\n".join(lines)


if __name__ == "__main__":
    main()
