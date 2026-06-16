"""Phase 4 — Thumbnails & multi-document contract.

Thumbnails are rendered inside the JS wrapper (the upstream render-prop API is
not expressible from Python), toggled by ``show_thumbnails`` with an optional
``horizontal_thumbnails`` layout. Multiple viewers are independent because each
``pdf_slick(...)`` instantiates its own ``usePDFSlick`` hook / Zustand store.
"""

from reflex_pdfslick import PdfSlick, pdf_slick


def test_thumbnail_props_exist():
    props = PdfSlick.get_props()
    assert "show_thumbnails" in props
    assert "horizontal_thumbnails" in props
    assert "thumbnail_width" in props


def test_multiple_instances_are_independent():
    a = pdf_slick(url="/a.pdf")
    b = pdf_slick(url="/b.pdf", show_thumbnails=True)
    # Distinct component objects, each carrying its own props → distinct
    # usePDFSlick hook / Zustand store at runtime.
    assert a is not b
    assert a.render() != b.render()


def test_horizontal_implies_thumbnails_in_demo_usage():
    # Sanity: a horizontal strip is only meaningful with thumbnails shown.
    component = pdf_slick(url="/a.pdf", show_thumbnails=True, horizontal_thumbnails=True)
    assert isinstance(component, PdfSlick)
