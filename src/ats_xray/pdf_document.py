"""One parsed PDF per analysis, however many detectors read it.

Naive extraction, layout-aware extraction, the repeated header and footer
check and the textless image check each opened the file for themselves, and
opening is cheap -- what is not is pdfplumber interpreting every page's
content stream the first time anything asks a page for its characters. That
happened once per detector per page: eight times for a two-page CV, and 93% of
the time the whole analysis took. pdfplumber caches the result on the page
object, so readers that share a document share the work.

``reading(path)`` opens the document and makes it the shared one for the
duration of a block; ``open_pdf(path)`` hands out that document inside such a
block and opens the file afresh outside one. Every detector opens through
``open_pdf``, so each of them still works called on its own, as the tests call
them, and the pipeline decides once where sharing starts and stops.

Shared per thread. Streamlit runs each browser session's script on a thread of
its own, and two sessions must never read each other's upload -- which could
only happen through a shared path, but a temp file name is the wrong thing to
rest that on.
"""

import os
import threading
from collections.abc import Iterator
from contextlib import contextmanager

import pdfplumber

_local = threading.local()


def _shared() -> dict[str, "pdfplumber.PDF"]:
    if not hasattr(_local, "documents"):
        _local.documents = {}
    return _local.documents


def _key(pdf_path: str) -> str:
    return os.path.normcase(os.path.abspath(os.fspath(pdf_path)))


@contextmanager
def reading(pdf_path: str) -> Iterator[None]:
    """Within this block, every ``open_pdf`` of this file gets one document."""
    documents, key = _shared(), _key(pdf_path)
    if key in documents:  # already shared by an enclosing block
        yield
        return
    with pdfplumber.open(pdf_path) as pdf:
        documents[key] = pdf
        try:
            yield
        finally:
            del documents[key]


@contextmanager
def open_pdf(pdf_path: str) -> Iterator["pdfplumber.PDF"]:
    """The shared document inside ``reading(pdf_path)``, a fresh one outside.

    The shared one is not closed on the way out: the block that opened it
    closes it, after the last detector is done.
    """
    shared = _shared().get(_key(pdf_path))
    if shared is not None:
        yield shared
        return
    with pdfplumber.open(pdf_path) as pdf:
        yield pdf
