"""DOCX text extraction, in two flavors.

``extract_docx_naive`` only reads ``document.paragraphs`` — a common
shortcut in simple parsers. Any text placed inside a Word **table** (a
popular way to build a two-column resume) never appears in ``.paragraphs``
at all, so it is silently dropped.

``extract_docx_full`` walks the document body in true XML order, handling
paragraphs and tables as they actually appear in the file, so nothing
inside a table is lost.
"""

import docx
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph


def extract_docx_naive(docx_path: str) -> str:
    document = docx.Document(docx_path)
    return "\n".join(p.text for p in document.paragraphs if p.text.strip())


def extract_docx_full(docx_path: str) -> str:
    document = docx.Document(docx_path)
    parts = []
    for child in document.element.body.iterchildren():
        if child.tag == qn("w:p"):
            text = Paragraph(child, document).text
            if text.strip():
                parts.append(text)
        elif child.tag == qn("w:tbl"):
            table = Table(child, document)
            for row in table.rows:
                cells = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if cells:
                    parts.append(" | ".join(cells))
    return "\n".join(parts)
