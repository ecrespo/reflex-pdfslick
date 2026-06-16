"""Phase 3 — Imperative control command serialization.

Python helpers build the declarative ``command`` objects the JS wrapper applies
against the ``pdfSlick`` instance (``specs/api/component-api.md`` §4). The
mapping is pinned here; the wrapper-side dispatch is validated in the demo/build.
"""

from reflex_pdfslick import PdfSlick, ScrollMode, SpreadMode
from reflex_pdfslick import commands as cmd


def test_component_exposes_command_prop():
    # The declarative control channel the helpers feed into.
    assert "command" in PdfSlick.get_props()


def test_goto_page():
    assert cmd.goto_page(3) == {"action": "goto", "page": 3}


def test_next_and_prev():
    assert cmd.next_page() == {"action": "next"}
    assert cmd.prev_page() == {"action": "prev"}


def test_zoom_in_out():
    assert cmd.zoom_in() == {"action": "zoomIn"}
    assert cmd.zoom_out() == {"action": "zoomOut"}


def test_zoom_preset():
    assert cmd.set_zoom_preset("page-fit") == {"action": "zoomPreset", "value": "page-fit"}


def test_zoom_value():
    assert cmd.set_zoom_value(1.5) == {"action": "zoomValue", "value": 1.5}


def test_rotate():
    assert cmd.rotate(90) == {"action": "rotate", "degrees": 90}
    assert cmd.rotate(-90) == {"action": "rotate", "degrees": -90}


def test_scroll_mode_uses_enum_value():
    assert cmd.set_scroll_mode(ScrollMode.HORIZONTAL) == {"action": "scrollMode", "mode": 1}
    # Plain ints accepted too.
    assert cmd.set_scroll_mode(2) == {"action": "scrollMode", "mode": 2}


def test_spread_mode_uses_enum_value():
    assert cmd.set_spread_mode(SpreadMode.ODD) == {"action": "spreadMode", "mode": 1}


def test_print_and_download():
    assert cmd.print_document() == {"action": "print"}
    assert cmd.download() == {"action": "download"}


def test_commands_are_plain_json_serializable():
    import json

    payload = json.dumps(cmd.set_scroll_mode(ScrollMode.PAGE))
    assert json.loads(payload) == {"action": "scrollMode", "mode": 3}
