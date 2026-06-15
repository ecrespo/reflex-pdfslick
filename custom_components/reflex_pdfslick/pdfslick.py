"""The ``PdfSlick`` Reflex component (scaffold).

This module defines the **public API surface** of the component. The runtime
wiring (local ``PdfSlickWrapper.tsx`` + build integration) is implemented in
Phase 1 of ``specs/plans/implementation-plan.md``.

Design summary (see ``specs/technical/architecture.md`` for the full rationale):

- PDFSlick's public entry point is the **hook** ``usePDFSlick(url, options)``,
  not a drop-in component, and its ``<PDFSlickThumbnails>`` uses a render-prop
  child that cannot be expressed from Python. So we ship a small local React
  wrapper (``js/PdfSlickWrapper.tsx``) that calls the hook internally, renders
  ``<PDFSlickViewer>``, subscribes to ``usePDFSlickStore`` selectors, and
  exposes a clean prop/event API.
- PDF.js is browser-only (touches ``window``/``document``/canvas), so the
  component MUST be a ``rx.NoSSRComponent`` to avoid SSR crashes.
- The required stylesheet ``@pdfslick/react/dist/pdf_viewer.css`` is imported
  once via ``add_imports``.
"""

from __future__ import annotations

from typing import Any

import reflex as rx

# Pin the upstream npm package for reproducible builds.
PDFSLICK_REACT = "@pdfslick/react@4.0.0"
PDFSLICK_CSS = "@pdfslick/react/dist/pdf_viewer.css"


class PdfSlick(rx.NoSSRComponent):
    """Reactive PDF viewer wrapping ``@pdfslick/react``.

    NOTE: This is a Phase-0 scaffold. The class documents the intended prop and
    event contract; ``create`` raises ``NotImplementedError`` until the Phase-1
    JS wrapper is integrated. See ``specs/`` for the authoritative contract.
    """

    # --- Library wiring (Phase 1) -------------------------------------------
    # The runtime component is the local wrapper, with the npm package declared
    # as a dependency so Reflex installs it:
    #
    #   _wrapper = rx.asset("./js/PdfSlickWrapper.tsx", shared=True)
    #   library = f"$/public{_wrapper}"
    #   tag = "PdfSlickWrapper"
    #   lib_dependencies = [PDFSLICK_REACT]
    #
    # For the scaffold we point ``library`` at the package so the class is well
    # formed; ``create`` is guarded below.
    library = PDFSLICK_REACT
    tag = "PDFSlickViewer"

    # --- Props (camelCased to JS automatically) -----------------------------
    url: rx.Var[str]
    scale_value: rx.Var[str]
    single_page_viewer: rx.Var[bool]
    remove_page_borders: rx.Var[bool]
    thumbnail_width: rx.Var[int]
    show_thumbnails: rx.Var[bool]

    # --- Events -------------------------------------------------------------
    # Each forwards the JS callback's first argument to the Python handler.
    on_document_load: rx.EventHandler[lambda num_pages: [num_pages]]
    on_page_change: rx.EventHandler[lambda page: [page]]
    on_scale_change: rx.EventHandler[lambda scale: [scale]]
    on_error: rx.EventHandler[lambda err: [err]]

    def add_imports(self) -> dict[str, Any]:
        """Import PDFSlick's required stylesheet exactly once (Phase 1)."""
        return {"": PDFSLICK_CSS}

    @classmethod
    def create(cls, *children, **props) -> "PdfSlick":  # noqa: D401
        raise NotImplementedError(
            "reflex-pdfslick is in Phase 0 (specification + scaffold). The "
            "runtime wrapper lands in Phase 1 — see "
            "specs/plans/implementation-plan.md. The prop/event contract is "
            "documented in specs/api/component-api.md."
        )


# Snake_case factory following Reflex convention.
pdf_slick = PdfSlick.create
