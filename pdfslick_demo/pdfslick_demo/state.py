"""Reflex state for the demo gallery.

Each example keeps only the viewer slices it needs, synced via the component's
events, and drives the viewer through the declarative ``command`` prop (see
``reflex_pdfslick.commands``).
"""

from __future__ import annotations

import reflex as rx

from reflex_pdfslick import ScrollMode, SpreadMode, commands

# A CORS-friendly sample PDF (Mozilla pdf.js test document). Drop your own file
# in ``assets/`` and use ``/your.pdf`` to serve it locally instead.
SAMPLE_PDF = (
    "https://raw.githubusercontent.com/mozilla/pdf.js/ba2edeae/web/"
    "compressed.tracemonkey-pldi-09.pdf"
)
BAD_PDF = "/does-not-exist.pdf"


class ViewerState(rx.State):
    """Shared viewer state slice bound to the component events."""

    page_number: int = 1
    num_pages: int = 0
    scale: float = 1.0
    is_loaded: bool = False
    error: dict = {}
    title: str = ""
    author: str = ""

    # Declarative command sent to the viewer; ``{}`` means idle.
    command: dict = {}

    @rx.event
    def on_page_change(self, page: int):
        self.page_number = page

    @rx.event
    def on_document_load(self, num_pages: int):
        self.num_pages = num_pages
        self.is_loaded = True

    @rx.event
    def on_scale_change(self, scale: float):
        self.scale = scale

    @rx.event
    def on_error(self, err: dict):
        self.error = err

    @rx.event
    def on_metadata(self, meta: dict):
        self.title = meta.get("title", "") if isinstance(meta, dict) else ""
        self.author = meta.get("author", "") if isinstance(meta, dict) else ""

    # --- imperative controls via the command channel --------------------
    @rx.event
    def go_next(self):
        self.command = commands.next_page()

    @rx.event
    def go_prev(self):
        self.command = commands.prev_page()

    @rx.event
    def goto(self, page: int):
        self.command = commands.goto_page(page)

    @rx.event
    def zoom_in(self):
        self.command = commands.zoom_in()

    @rx.event
    def zoom_out(self):
        self.command = commands.zoom_out()

    @rx.event
    def set_preset(self, preset: str):
        self.command = commands.set_zoom_preset(preset)

    @rx.event
    def rotate_cw(self):
        self.command = commands.rotate(90)

    @rx.event
    def rotate_ccw(self):
        self.command = commands.rotate(-90)

    @rx.event
    def scroll_horizontal(self):
        self.command = commands.set_scroll_mode(ScrollMode.HORIZONTAL)

    @rx.event
    def scroll_vertical(self):
        self.command = commands.set_scroll_mode(ScrollMode.VERTICAL)

    @rx.event
    def spread_odd(self):
        self.command = commands.set_spread_mode(SpreadMode.ODD)

    @rx.event
    def spread_none(self):
        self.command = commands.set_spread_mode(SpreadMode.NONE)

    @rx.event
    def print_doc(self):
        self.command = commands.print_document()

    @rx.event
    def download_doc(self):
        self.command = commands.download()


class ErrorState(rx.State):
    """State for the error-handling example."""

    error: dict = {}

    @rx.var
    def has_error(self) -> bool:
        return bool(self.error)

    @rx.var
    def error_message(self) -> str:
        return self.error.get("message", "") if self.error else ""

    @rx.event
    def on_error(self, err: dict):
        self.error = err
