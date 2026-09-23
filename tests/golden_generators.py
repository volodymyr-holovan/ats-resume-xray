"""Generates labeled resume fixtures, one per documented parsing-risk
pattern the rule engine knows about (plus one clean control). Each
function writes a single fixture file to the given path.

Used by test_golden_fixtures.py to build known-good and known-broken
resumes and assert the rule engine reacts to each pattern — no more, no
less — so a future change that silently breaks a detector shows up as a
failing test instead of a quiet regression.

Not a test module itself (no test_ prefix), so pytest won't try to collect
it directly.
"""

from pathlib import Path

import docx
import reportlab
from docx.oxml import parse_xml
from docx.oxml.ns import nsmap
from PIL import Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def clean_single_column(path) -> None:
    """A well-formed, single-column resume with every expected section and
    contact field present. Nothing should trigger.
    """
    c = canvas.Canvas(str(path), pagesize=(400, 420))
    c.setFont("Helvetica", 12)
    c.drawString(30, 390, "Jane Doe")
    c.drawString(30, 370, "jane@example.com | +1 555 123 4567")
    c.drawString(30, 330, "Experience")
    c.drawString(30, 310, "Senior Engineer at Acme")
    c.drawString(30, 270, "Education")
    c.drawString(30, 250, "BSc Computer Science")
    c.drawString(30, 210, "Skills")
    c.drawString(30, 190, "Python, SQL")
    c.save()


def missing_optional_section(path) -> None:
    """A resume that simply never mentions Education — by the candidate's
    choice, not because of a formatting bug. Every rule that compares
    naive vs. layout-aware extraction must stay quiet here: a section
    that's absent from both readings isn't a parsing risk, just content
    the candidate didn't include.
    """
    c = canvas.Canvas(str(path), pagesize=(400, 300))
    c.setFont("Helvetica", 12)
    c.drawString(30, 270, "Jane Doe")
    c.drawString(30, 250, "jane@example.com | +1 555 123 4567")
    c.drawString(30, 210, "Experience")
    c.drawString(30, 190, "Senior Engineer at Acme")
    c.save()


def contact_with_only_email(path) -> None:
    """Only an email, no phone number. missing_contact_field should only
    fire when *both* are absent — a candidate reachable by one channel is
    still reachable.
    """
    c = canvas.Canvas(str(path), pagesize=(400, 300))
    c.setFont("Helvetica", 12)
    c.drawString(30, 270, "Jane Doe")
    c.drawString(30, 250, "jane@example.com")
    c.drawString(30, 210, "Experience")
    c.drawString(30, 190, "Senior Engineer at Acme")
    c.save()


def two_column_pdf(path) -> None:
    """A section header split across two columns: readable layout-aware,
    invisible under naive, order-blind extraction.
    """
    c = canvas.Canvas(str(path), pagesize=(500, 300))
    c.setFont("Helvetica", 12)
    c.drawString(30, 270, "Jane Doe")
    c.drawString(30, 250, "Experience")
    c.drawString(280, 270, "jane@example.com")
    c.drawString(280, 250, "+1 555 123 4567")
    c.save()


def missing_contact(path) -> None:
    """A resume with no email or phone number anywhere in the document."""
    c = canvas.Canvas(str(path), pagesize=(400, 300))
    c.setFont("Helvetica", 12)
    c.drawString(30, 270, "Jane Doe")
    c.drawString(30, 230, "Experience")
    c.drawString(30, 210, "Senior Engineer at Acme")
    c.save()


def pdf_textless_image(path) -> None:
    """A name banner exported as a picture instead of real text, with the
    rest of the resume as normal, readable text.
    """
    image_path = Path(path).with_suffix(".png")
    Image.new("RGB", (300, 80), color="white").save(image_path)

    c = canvas.Canvas(str(path), pagesize=(400, 300))
    c.drawImage(str(image_path), 30, 220, width=300, height=60)
    c.setFont("Helvetica", 10)
    c.drawString(30, 190, "jane@example.com | +1 555 123 4567")
    c.drawString(30, 150, "Experience")
    c.drawString(30, 130, "Senior Engineer at Acme")
    c.save()
    image_path.unlink()


def pdf_repeated_header_footer(path) -> None:
    """A footer with contact info repeating verbatim across two pages —
    single-column body text throughout, so this isolates the
    repeated-footer signal without also tripping the column-mangling one.
    """
    c = canvas.Canvas(str(path), pagesize=(400, 300))
    for page_num in (1, 2):
        c.setFont("Helvetica", 12)
        c.drawString(30, 270, "Jane Doe")
        c.drawString(30, 250, "Experience" if page_num == 1 else "Education")
        c.drawString(30, 150, f"Body content page {page_num}")
        c.drawString(30, 20, "jane@example.com | +1 555 123 4567")
        if page_num == 1:
            c.showPage()
    c.save()


def docx_with_table(path) -> None:
    """Resume content placed inside a DOCX table."""
    document = docx.Document()
    document.add_paragraph("Jane Doe")
    document.add_paragraph("jane@example.com, +1 555 123 4567")
    table = document.add_table(rows=1, cols=2)
    table.rows[0].cells[0].text = "Skills"
    table.rows[0].cells[1].text = "Python, SQL"
    document.save(str(path))


def docx_contact_in_header(path) -> None:
    """Contact info that lives only in the header: invisible to body-only
    extraction, and genuinely unreachable since it appears nowhere else.
    """
    document = docx.Document()
    document.sections[0].header.paragraphs[0].text = "jane@example.com | +1 555 123 4567"
    document.add_paragraph("Jane Doe")
    document.add_paragraph("Experience")
    document.add_paragraph("Senior Engineer at Acme")
    document.save(str(path))


def docx_text_box(path) -> None:
    """Resume content placed inside a Word text box."""
    document = docx.Document()
    document.add_paragraph("Jane Doe")
    document.add_paragraph("jane@example.com, +1 555 123 4567")
    document.add_paragraph("Experience")
    document.add_paragraph("Senior Engineer at Acme")
    txbx_xml = (
        f'<w:txbxContent xmlns:w="{nsmap["w"]}">'
        "<w:p><w:r><w:t>Skills: Python, SQL, Docker</w:t></w:r></w:p>"
        "</w:txbxContent>"
    )
    document.element.body.append(parse_xml(txbx_xml))
    document.save(str(path))


def pdf_unembedded_font(path) -> None:
    """A clean single-column resume set in a font that is referenced and
    never embedded.

    Written out byte by byte because nothing in this project can produce
    one: reportlab embeds every TrueType face it is handed, and the only
    fonts it references without embedding are the standard fourteen, which
    the rule exempts. That is why a high-severity rule went this long with
    no golden fixture — not because the case is rare in the wild, but
    because the fixture could not be generated the usual way.

    The font carries a FontDescriptor with metrics and no font program,
    which is what a real non-embedded font looks like, rather than no
    descriptor at all.
    """
    lines = [
        (30, 390, "Jane Doe"),
        (30, 370, "jane@example.com | +1 555 123 4567"),
        (30, 330, "Experience"),
        (30, 310, "Senior Engineer at Acme"),
        (30, 270, "Education"),
        (30, 250, "BSc Computer Science"),
        (30, 210, "Skills"),
        (30, 190, "Python, SQL"),
    ]
    newline = b"\n"
    content = newline.join(
        f"BT /F1 12 Tf {x} {y} Td ({text}) Tj ET".encode("latin-1")
        for x, y, text in lines
    )
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 400 420] "
        b"/Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>",
        b"<< /Length " + str(len(content)).encode() + b" >>"
        + newline + b"stream" + newline + content + newline + b"endstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Frutiger-Light /FontDescriptor 6 0 R >>",
        b"<< /Type /FontDescriptor /FontName /Frutiger-Light /Flags 32 "
        b"/FontBBox [-100 -250 1000 900] /ItalicAngle 0 /Ascent 900 "
        b"/Descent -250 /CapHeight 700 /StemV 80 >>",
    ]

    out = bytearray(b"%PDF-1.4" + newline)
    offsets = []
    for number, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += str(number).encode() + b" 0 obj" + newline + body + newline + b"endobj" + newline

    xref_at = len(out)
    size = str(len(objects) + 1).encode()
    out += b"xref" + newline + b"0 " + size + newline + b"0000000000 65535 f " + newline
    for offset in offsets:
        out += str(offset).zfill(10).encode() + b" 00000 n " + newline
    out += b"trailer" + newline + b"<< /Size " + size + b" /Root 1 0 R >>" + newline
    out += b"startxref" + newline + str(xref_at).encode() + newline + b"%%EOF" + newline

    Path(path).write_bytes(bytes(out))


def pdf_contact_only_as_link(path) -> None:
    """A tidy resume whose only route to the candidate is a profile URL.

    The link text is what a parser reads; the address behind it lives in an
    annotation most parsers never open. Written out as text rather than as a
    real annotation for that reason -- the fixture is about what the reader
    gets, and what it gets is a string that is not an email address.
    """
    c = canvas.Canvas(str(path), pagesize=(400, 420))
    c.setFont("Helvetica", 12)
    c.drawString(30, 390, "Jane Doe")
    c.drawString(30, 370, "linkedin.com/in/janedoe")
    c.drawString(30, 330, "Experience")
    c.drawString(30, 310, "Senior Engineer at Acme")
    c.drawString(30, 270, "Education")
    c.drawString(30, 250, "BSc Computer Science")
    c.drawString(30, 210, "Skills")
    c.drawString(30, 190, "Python, SQL")
    c.save()


def pdf_invented_headings(path) -> None:
    """Every section label is a phrase the parser has never heard of.

    "My Journey" and "What I Bring" read beautifully and leave the document
    as one undifferentiated block with no history in it. Each label is
    followed by a dated entry, which is the signal that tells the detector a
    heading-shaped line was labelling a section rather than being a job
    title.
    """
    c = canvas.Canvas(str(path), pagesize=(400, 420))
    c.setFont("Helvetica", 12)
    c.drawString(30, 390, "Jane Doe")
    c.drawString(30, 370, "jane@example.com | +1 555 123 4567")
    c.drawString(30, 330, "My Journey")
    c.drawString(30, 310, "Senior Engineer at Acme 03/2019 - 07/2024")
    c.drawString(30, 270, "Where I Studied")
    c.drawString(30, 250, "BSc Computer Science 09/2014 - 06/2018")
    c.drawString(30, 210, "What I Bring")
    c.drawString(30, 190, "Python, SQL")
    c.save()


def pdf_broken_characters(path) -> None:
    """A soft hyphen in the middle of a word nobody will ever search for.

    It is invisible unless the line happens to break there, and a search for
    "Responsible" does not find "Respon-sible" with an invisible hyphen in
    the join. The character is built with chr() rather than pasted, so that
    this file stays greppable and no editor quietly removes the one thing
    the fixture is for.

    Set in an embedded TrueType face rather than Helvetica, and that is not
    decoration. Drawn in a standard-14 font the soft hyphen comes back out
    of the PDF as an ordinary space, so the fault the fixture exists to
    carry simply is not there. Only a font with a real glyph for it and a
    character map that says so preserves it -- which is also why this turns
    up in documents from design tools and not in plain exports.

    A soft hyphen and not a zero-width space: a zero-width space draws no
    glyph at all, so it never becomes a word and never reaches the extracted
    text of a PDF. That one can only be tested through a DOCX.
    """
    soft_hyphen = chr(0x00AD)
    vera = Path(reportlab.__file__).parent / "fonts" / "Vera.ttf"
    pdfmetrics.registerFont(TTFont("Vera", str(vera)))

    c = canvas.Canvas(str(path), pagesize=(400, 420))
    c.setFont("Vera", 12)
    c.drawString(30, 390, "Jane Doe")
    c.drawString(30, 370, "jane@example.com | +1 555 123 4567")
    c.drawString(30, 330, "Experience")
    c.drawString(30, 310, f"Respon{soft_hyphen}sible for the payments platform at Acme")
    c.drawString(30, 270, "Education")
    c.drawString(30, 250, "BSc Computer Science")
    c.drawString(30, 210, "Skills")
    c.drawString(30, 190, "Python, SQL")
    c.save()
