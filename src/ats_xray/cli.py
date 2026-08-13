"""Command-line entry point: ``atsxray path/to/resume.pdf``."""

import argparse
from pathlib import Path

from .docx_extract import extract_docx_full, extract_docx_naive
from .extract import extract_layout_aware, extract_naive

SEPARATOR = "=" * 30


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="atsxray",
        description="Show what a resume-parsing pipeline actually extracts from your file.",
    )
    parser.add_argument("file", help="Path to a .pdf or .docx resume")
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


if __name__ == "__main__":
    main()
