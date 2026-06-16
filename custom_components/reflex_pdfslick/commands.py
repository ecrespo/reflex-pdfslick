"""Declarative imperative-control commands for ``PdfSlick``.

PDFSlick's imperative actions live on the ``pdfSlick`` store instance, which
stays in JS. To drive them from Python we send a small JSON ``command`` object
into the component's ``command`` prop; the JS wrapper watches it and applies the
matching action once (apply-then-clear by command identity).

These helpers build those objects so app code never hand-writes the action
strings. Bind the result to ``PdfSlick(..., command=State.command)`` and set
``State.command`` from an event handler::

    @rx.event
    def go_next(self):
        self.command = commands.next_page()

The action vocabulary mirrors ``specs/api/component-api.md`` §4 and the switch in
``js/PdfSlickWrapper.tsx``. ``None`` is the idle/cleared value (no-op).

References:
- ``specs/api/component-api.md`` §4
- ``specs/technical/architecture.md`` §4.5
"""

from __future__ import annotations

from typing import Any

Command = dict[str, Any]


def goto_page(page: int) -> Command:
    """Jump to a 1-based page number (``pdfSlick.gotoPage(page)``)."""
    return {"action": "goto", "page": int(page)}


def next_page() -> Command:
    """Go to the next page (clamped to the last page)."""
    return {"action": "next"}


def prev_page() -> Command:
    """Go to the previous page (clamped to the first page)."""
    return {"action": "prev"}


def zoom_in() -> Command:
    """Step zoom in (``viewer.increaseScale()``)."""
    return {"action": "zoomIn"}


def zoom_out() -> Command:
    """Step zoom out (``viewer.decreaseScale()``)."""
    return {"action": "zoomOut"}


def set_zoom_preset(preset: str) -> Command:
    """Set a named zoom preset (``pdfSlick.currentScaleValue = preset``).

    ``preset`` is one of ``"auto" | "page-actual" | "page-fit" | "page-width"``
    (see :class:`~reflex_pdfslick.ScaleValue`).
    """
    return {"action": "zoomPreset", "value": str(preset)}


def set_zoom_value(scale: float) -> Command:
    """Set an absolute numeric zoom (``pdfSlick.currentScale = scale``)."""
    return {"action": "zoomValue", "value": float(scale)}


def rotate(degrees: int) -> Command:
    """Rotate pages by a relative delta in degrees (e.g. ``90`` / ``-90``)."""
    return {"action": "rotate", "degrees": int(degrees)}


def set_scroll_mode(mode: int) -> Command:
    """Set the scroll mode (``pdfSlick.setScrollMode``).

    Accepts a :class:`~reflex_pdfslick.ScrollMode` or a plain int.
    """
    return {"action": "scrollMode", "mode": int(mode)}


def set_spread_mode(mode: int) -> Command:
    """Set the spread mode (``pdfSlick.setSpreadMode``).

    Accepts a :class:`~reflex_pdfslick.SpreadMode` or a plain int.
    """
    return {"action": "spreadMode", "mode": int(mode)}


def print_document() -> Command:
    """Open the print dialog (``pdfSlick.triggerPrinting()``)."""
    return {"action": "print"}


def download() -> Command:
    """Download / save the document (``pdfSlick.downloadOrSave()``)."""
    return {"action": "download"}
