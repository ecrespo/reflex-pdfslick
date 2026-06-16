"""Phase 1 — Core wrapper contract.

These tests pin the Reflex wiring described in ``specs/technical/architecture.md``
(§4.3) and the prop surface in ``specs/api/component-api.md`` (§2). They run
without a frontend build: they only introspect the ``PdfSlick`` component class.
"""

import reflex as rx

from reflex_pdfslick import PdfSlick, pdf_slick
from reflex_pdfslick.pdfslick import PDFJS_DIST, PDFSLICK_CSS, PDFSLICK_REACT


def test_create_returns_component_instance():
    # Phase 1 replaces the Phase-0 NotImplementedError scaffold: creating the
    # component now yields a real Reflex component.
    component = pdf_slick(url="/sample.pdf")
    assert isinstance(component, PdfSlick)
    assert isinstance(component, rx.Component)


def test_library_points_at_local_wrapper():
    # The runtime component is the local .tsx wrapper, referenced via the
    # `$/public` importable path — not the npm package directly.
    assert PdfSlick.library is not None
    assert PdfSlick.library.startswith("$/public")
    assert PdfSlick.library.endswith("PdfSlickWrapper.tsx")


def test_tag_is_the_wrapper_component():
    assert PdfSlick.tag == "PdfSlickWrapper"


def test_npm_dependency_is_pinned():
    assert PDFSLICK_REACT == "@pdfslick/react@4.0.0"
    assert PDFSLICK_REACT in PdfSlick.lib_dependencies


def test_pdfjs_worker_dependency_is_declared():
    # Needed so the wrapper can import the PDF.js worker as a Vite asset and
    # override PDFSlick's broken default workerSrc (worker version must match
    # @pdfslick/core's pdfjs-dist).
    assert PDFJS_DIST.startswith("pdfjs-dist@")
    assert PDFJS_DIST in PdfSlick.lib_dependencies


def test_core_props_are_declared():
    props = PdfSlick.get_props()
    for prop in [
        "url",
        "scale_value",
        "single_page_viewer",
        "remove_page_borders",
        "thumbnail_width",
        "show_thumbnails",
    ]:
        assert prop in props, prop


def test_css_is_imported_once():
    imports = PdfSlick.create(url="/sample.pdf").add_imports()
    # CSS is imported for side effects under the empty-string import key.
    assert PDFSLICK_CSS in imports.get("", [])
