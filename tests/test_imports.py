"""Smoke tests: the package imports and exposes its public surface."""

import reflex_pdfslick as rp


def test_public_symbols_exist():
    for name in [
        "pdf_slick",
        "PdfSlick",
        "PdfSlickOptions",
        "ScaleValue",
        "ScrollMode",
        "SpreadMode",
    ]:
        assert hasattr(rp, name), name


def test_version_present():
    assert isinstance(rp.__version__, str)
    assert rp.__version__


def test_factory_is_component_create():
    assert rp.pdf_slick == rp.PdfSlick.create


def test_create_builds_a_component():
    # Phase 1+: the runtime wrapper is wired, so creating the component yields a
    # real Reflex component (the Phase-0 NotImplementedError guard is gone).
    component = rp.pdf_slick(url="/sample.pdf")
    assert isinstance(component, rp.PdfSlick)
