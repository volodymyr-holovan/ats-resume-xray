import pytest
from PIL import Image
from reportlab.pdfgen import canvas

from ats_xray.engine import Finding, run_rules
from ats_xray.overlay import render_pages_with_findings
from ats_xray.pipeline import extract_text
from ats_xray.regions import Region, bounding_region, region_from_words
from ats_xray.rule import get_rule


def test_region_padded_grows_every_side():
    padded = Region(page=1, x0=10, top=20, x1=30, bottom=40).padded(5)

    assert (padded.x0, padded.top, padded.x1, padded.bottom) == (5, 15, 35, 45)


def test_bounding_region_merges_same_page():
    merged = bounding_region(
        [Region(page=2, x0=10, top=10, x1=20, bottom=20), Region(page=2, x0=50, top=5, x1=60, bottom=30)]
    )

    assert merged == Region(page=2, x0=10, top=5, x1=60, bottom=30)


def test_bounding_region_empty_is_none():
    assert bounding_region([]) is None


def test_bounding_region_rejects_cross_page_merge():
    with pytest.raises(ValueError):
        bounding_region([Region(page=1, x0=0, top=0, x1=1, bottom=1), Region(page=2, x0=0, top=0, x1=1, bottom=1)])


def test_region_from_words():
    words = [
        {"x0": 10, "top": 20, "x1": 40, "bottom": 32},
        {"x0": 45, "top": 21, "x1": 70, "bottom": 33},
    ]

    assert region_from_words(3, words) == Region(page=3, x0=10, top=20, x1=70, bottom=33)


def _two_column_pdf(path):
    c = canvas.Canvas(str(path), pagesize=(500, 300))
    c.setFont("Helvetica", 12)
    c.drawString(30, 270, "Jane Doe")
    c.drawString(30, 250, "Experience")
    c.drawString(280, 270, "jane@example.com")
    c.drawString(280, 250, "+1 555 123 4567")
    c.save()


def test_section_finding_region_stays_inside_its_own_column(tmp_path):
    """A section in the left column must not be reported as covering the
    right-hand one, however tall it is.
    """
    pdf_path = tmp_path / "resume.pdf"
    _two_column_pdf(pdf_path)

    naive, aware = extract_text(str(pdf_path))
    findings = run_rules(str(pdf_path), naive, aware)

    finding = next(f for f in findings if f.rule.id == "section_missing_under_naive_parsing")
    assert finding.regions
    region = finding.regions[0]
    assert region.page == 1
    assert region.x0 >= 25
    assert region.x1 < 280, "the box must not reach into the right-hand column"


def test_section_region_covers_the_body_not_just_the_heading(tmp_path):
    """The point of the box is to show the content at risk, so it has to
    extend past the heading line and stop at the next heading.
    """
    pdf_path = tmp_path / "resume.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=(500, 400))
    c.setFont("Helvetica", 12)
    c.drawString(30, 370, "Jane Doe")
    c.drawString(30, 340, "Experience")
    c.drawString(30, 320, "Senior Engineer at Acme")
    c.drawString(30, 300, "Built the billing pipeline")
    c.drawString(30, 250, "Education")
    c.drawString(30, 230, "BSc Computer Science")
    # Right-hand column, to make the sections vanish under naive reading.
    c.drawString(300, 370, "jane@example.com")
    c.drawString(300, 340, "+1 555 123 4567")
    c.save()

    naive, aware = extract_text(str(pdf_path))
    findings = run_rules(str(pdf_path), naive, aware)
    finding = next(f for f in findings if f.rule.id == "section_missing_under_naive_parsing")

    experience = min(finding.regions, key=lambda r: r.top)
    height = experience.bottom - experience.top

    assert height > 40, f"expected the box to cover the section body, got {height:.0f}pt"
    assert experience.bottom < 160, "the Experience box must stop before the Education heading"


def test_render_marks_only_pages_that_have_findings(tmp_path):
    pdf_path = tmp_path / "resume.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=(300, 200))
    c.drawString(30, 150, "Page one")
    c.showPage()
    c.drawString(30, 150, "Page two")
    c.save()

    finding = Finding(
        rule=get_rule("pdf_textless_image"),
        evidence="test",
        regions=(Region(page=2, x0=10, top=10, x1=100, bottom=50),),
    )

    pages = render_pages_with_findings(str(pdf_path), [finding])

    assert [p.page_number for p in pages] == [1, 2]
    assert pages[0].marked_findings == []
    assert pages[1].marked_findings == [finding]


def test_render_draws_visible_pixels_where_the_region_is(tmp_path):
    """A near-blank page plus one region should come back with red pixels on
    the box and none far outside it.
    """
    pdf_path = tmp_path / "blank.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=(200, 200))
    # reportlab drops a page with no content at all, so anchor one mark in a
    # corner well away from both the region and the sampled points below.
    c.setFont("Helvetica", 6)
    c.drawString(5, 5, ".")
    c.save()

    finding = Finding(
        rule=get_rule("pdf_textless_image"),  # high -> red
        evidence="test",
        regions=(Region(page=1, x0=20, top=20, x1=80, bottom=60),),
    )

    page = render_pages_with_findings(str(pdf_path), [finding])[0]
    image = page.image
    scale = image.width / 200

    # The fill tint is deliberately faint so text under it stays readable; the
    # outline is the strong mark. Look for the reddest pixel in the region
    # rather than sampling one point and guessing where the stroke landed.
    pixels = [
        image.getpixel((x, y))
        for x in range(int(15 * scale), int(85 * scale))
        for y in range(int(15 * scale), int(65 * scale))
    ]
    reddest = max(pixels, key=lambda px: px[0] - (px[1] + px[2]) / 2)
    far_outside = image.getpixel((int(150 * scale), int(150 * scale)))

    assert reddest[0] > 150 and reddest[1] < 100, f"expected a strong red outline pixel, got {reddest}"
    assert far_outside == (255, 255, 255)


def test_render_handles_a_pdf_with_no_findings(tmp_path):
    pdf_path = tmp_path / "clean.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=(200, 200))
    c.drawString(20, 100, "Nothing wrong here")
    c.save()

    pages = render_pages_with_findings(str(pdf_path), [])

    assert len(pages) == 1
    assert pages[0].marked_findings == []
    assert isinstance(pages[0].image, Image.Image)
