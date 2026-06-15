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


def test_phase0_create_raises_not_implemented():
    # Phase-0 contract: the runtime wrapper lands in Phase 1, so creating the
    # component raises a clear NotImplementedError until then.
    import pytest

    with pytest.raises(NotImplementedError):
        rp.pdf_slick(url="/sample.pdf")
