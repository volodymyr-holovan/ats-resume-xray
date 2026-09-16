"""One parsed PDF per analysis.

The promise ``pdf_document`` makes is a performance one, and a performance
promise nobody measures is broken by the next detector that opens the file
itself. So the first test counts the expensive step directly -- pdfplumber
interpreting a page's content stream -- across a whole analysis.
"""

import threading

import pdfplumber
import pytest
from pdfplumber.page import Page
from reportlab.pdfgen import canvas

from ats_xray.pdf_document import _shared, open_pdf, reading
from ats_xray.pipeline import analyze_path


@pytest.fixture
def two_pages(tmp_path):
    path = tmp_path / "two_pages.pdf"
    page = canvas.Canvas(str(path), pagesize=(595, 842))
    for number in (1, 2):
        page.setFont("Helvetica", 11)
        page.drawString(57, 810, "Anna Bergmann · anna@example.de · +49 421 1234567")
        page.drawString(57, 700, "BERUFSERFAHRUNG" if number == 1 else "AUSBILDUNG")
        page.drawString(57, 680, f"Zeile auf Seite {number}")
        page.drawString(57, 30, f"Seite {number} von 2")
        page.showPage()
    page.save()
    return str(path)


def test_a_whole_analysis_interprets_each_page_once(two_pages, monkeypatch):
    """Four detectors read every page. Before the document was shared this
    counted eight for two pages; the number that matters is the page count."""
    interpreted = []
    original = Page.parse_objects

    def counting(self):
        interpreted.append(self.page_number)
        return original(self)

    monkeypatch.setattr(Page, "parse_objects", counting)
    analyze_path(two_pages)

    assert sorted(interpreted) == [1, 2]


def test_every_open_inside_the_block_gets_the_same_document(two_pages):
    with reading(two_pages):
        with open_pdf(two_pages) as first, open_pdf(two_pages) as second:
            assert first is second


def test_outside_a_block_each_open_is_its_own_and_is_closed(two_pages):
    with open_pdf(two_pages) as first:
        pass
    with open_pdf(two_pages) as second:
        pass
    assert first is not second
    assert first.stream.closed and second.stream.closed


def test_the_shared_document_is_closed_and_forgotten_after_the_block(two_pages):
    with reading(two_pages):
        with open_pdf(two_pages) as shared:
            pass
        assert not shared.stream.closed, "a detector's own block closed the shared document"
    assert shared.stream.closed
    assert _shared() == {}


def test_a_nested_block_does_not_close_the_outer_one(two_pages):
    with reading(two_pages):
        with reading(two_pages):
            with open_pdf(two_pages) as inner:
                pass
        with open_pdf(two_pages) as outer:
            assert outer is inner
            assert not outer.stream.closed


def test_the_same_path_spelled_differently_is_the_same_document(two_pages, monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    with reading(two_pages):
        with open_pdf("two_pages.pdf") as relative, open_pdf(two_pages) as absolute:
            assert relative is absolute


def test_another_thread_never_sees_this_threads_document(two_pages):
    """Streamlit runs each browser session on a thread of its own."""
    seen = {}

    def other_session():
        with open_pdf(two_pages) as pdf:
            seen["document"] = pdf

    with reading(two_pages):
        with open_pdf(two_pages) as mine:
            worker = threading.Thread(target=other_session)
            worker.start()
            worker.join()

    assert seen["document"] is not mine


def test_a_file_that_is_not_a_pdf_fails_where_it_is_opened(tmp_path):
    broken = tmp_path / "broken.pdf"
    broken.write_bytes(b"%PDF-1.4\nnot really a pdf\n")
    with pytest.raises(Exception):
        with reading(str(broken)):
            pass
    assert _shared() == {}
    # And pdfplumber agrees it is unreadable, so this is not a new failure.
    with pytest.raises(Exception):
        pdfplumber.open(str(broken)).pages
