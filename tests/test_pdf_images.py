from PIL import Image
from reportlab.pdfgen import canvas

from ats_xray.pdf_images import _overlaps, find_large_textless_images


def test_overlaps_true_when_boxes_intersect():
    image = {"x0": 0, "x1": 100, "top": 0, "bottom": 50}
    word = {"x0": 40, "x1": 60, "top": 10, "bottom": 20}
    assert _overlaps(image, word) is True


def test_overlaps_false_when_boxes_disjoint():
    image = {"x0": 0, "x1": 100, "top": 0, "bottom": 50}
    word = {"x0": 200, "x1": 240, "top": 10, "bottom": 20}
    assert _overlaps(image, word) is False


def test_find_large_textless_images_flags_large_image_without_text(tmp_path):
    image_path = tmp_path / "banner.png"
    Image.new("RGB", (300, 80), color="white").save(image_path)

    pdf_path = tmp_path / "resume.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=(400, 300))
    c.drawImage(str(image_path), 30, 220, width=300, height=60)
    c.setFont("Helvetica", 10)
    c.drawString(30, 100, "Unrelated body text lower on the page.")
    c.save()

    findings = find_large_textless_images(str(pdf_path))
    assert len(findings) == 1
    assert findings[0]["page"] == 1


def test_find_large_textless_images_ignores_small_images(tmp_path):
    image_path = tmp_path / "icon.png"
    Image.new("RGB", (10, 10), color="black").save(image_path)

    pdf_path = tmp_path / "resume.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=(400, 300))
    c.drawImage(str(image_path), 30, 270, width=10, height=10)
    c.setFont("Helvetica", 10)
    c.drawString(30, 100, "Body text.")
    c.save()

    assert find_large_textless_images(str(pdf_path)) == []


def test_find_large_textless_images_ignores_image_with_overlapping_text(tmp_path):
    image_path = tmp_path / "photo.png"
    Image.new("RGB", (300, 80), color="white").save(image_path)

    pdf_path = tmp_path / "resume.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=(400, 300))
    c.drawImage(str(image_path), 30, 220, width=300, height=60)
    c.setFont("Helvetica", 10)
    c.drawString(40, 240, "Caption inside the image area")
    c.save()

    assert find_large_textless_images(str(pdf_path)) == []
