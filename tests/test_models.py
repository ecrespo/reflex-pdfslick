"""Unit tests for enums and options — runnable without a frontend build."""

from reflex_pdfslick import ScaleValue, ScrollMode, SpreadMode
from reflex_pdfslick import PdfSlickOptions


def test_scroll_mode_values():
    assert ScrollMode.VERTICAL == 0
    assert ScrollMode.HORIZONTAL == 1
    assert ScrollMode.WRAPPED == 2
    assert ScrollMode.PAGE == 3


def test_spread_mode_values():
    assert SpreadMode.NONE == 0
    assert SpreadMode.ODD == 1
    assert SpreadMode.EVEN == 2


def test_scale_value_strings():
    assert ScaleValue.AUTO == "auto"
    assert ScaleValue.PAGE_FIT == "page-fit"
    assert ScaleValue.PAGE_WIDTH == "page-width"
    assert ScaleValue.PAGE_ACTUAL == "page-actual"
    assert str(ScaleValue.PAGE_FIT) == "page-fit"


def test_options_defaults_are_optional():
    opts = PdfSlickOptions()
    assert opts.scale_value is None
    assert opts.single_page_viewer is None
    assert opts.extra == {}


def test_options_accepts_values():
    opts = PdfSlickOptions(scale_value="page-fit", single_page_viewer=True, thumbnail_width=200)
    assert opts.scale_value == "page-fit"
    assert opts.single_page_viewer is True
    assert opts.thumbnail_width == 200
