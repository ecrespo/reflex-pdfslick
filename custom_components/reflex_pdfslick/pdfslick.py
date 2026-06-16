"""The ``PdfSlick`` Reflex component.

PDFSlick's public entry point is the **hook** ``usePDFSlick(url, options)``, not
a drop-in component, and its ``<PDFSlickThumbnails>`` uses a render-prop child
that cannot be expressed from Python. So we ship a small local React wrapper
(``PdfSlickWrapper.tsx``, beside this module) that calls the hook internally,
renders
``<PDFSlickViewer>`` (+ optional thumbnails), subscribes to ``usePDFSlickStore``
selectors, and exposes a clean prop/event API. See
``specs/technical/architecture.md`` for the full rationale.

Wiring (Reflex 0.9.x):

- ``library`` points at the local wrapper via ``rx.asset(..., shared=True)``'s
  ``$/public`` importable path; the npm package is declared in
  ``lib_dependencies`` so Reflex installs it.
- PDF.js is browser-only (touches ``window``/``document``/canvas), so the
  component is a ``rx.NoSSRComponent`` (emits ``next/dynamic(..., {ssr:false})``).
- The required stylesheet ``@pdfslick/react/dist/pdf_viewer.css`` is imported
  once via ``add_imports``.
"""

from __future__ import annotations

from typing import Any

import reflex as rx

# Pin the upstream npm package for reproducible builds.
PDFSLICK_REACT = "@pdfslick/react@4.0.0"
PDFSLICK_CSS = "@pdfslick/react/dist/pdf_viewer.css"
# Declared so the wrapper can import the PDF.js worker as a Vite asset and
# override PDFSlick's broken default ``workerSrc``. The caret range matches
# ``@pdfslick/core``'s own dependency so the installer resolves a single shared
# copy — guaranteeing the worker version matches the PDF.js API version.
PDFJS_DIST = "pdfjs-dist@^6.0.227"

# Resolve the local JS wrapper into a build-time importable module path
# ("$/public/...") so Reflex bundles our source instead of trying to import a
# named export from the npm package.
_WRAPPER_ASSET = rx.asset("PdfSlickWrapper.tsx", shared=True)


class PdfSlick(rx.NoSSRComponent):
    """Reactive PDF viewer wrapping ``@pdfslick/react``."""

    # --- Library wiring -----------------------------------------------------
    library = _WRAPPER_ASSET.importable_path
    tag = "PdfSlickWrapper"
    is_default = True
    lib_dependencies = [PDFSLICK_REACT, PDFJS_DIST]

    # --- Props (camelCased to JS automatically) -----------------------------
    url: rx.Var[str]
    scale_value: rx.Var[str]
    single_page_viewer: rx.Var[bool]
    remove_page_borders: rx.Var[bool]
    thumbnail_width: rx.Var[int]
    show_thumbnails: rx.Var[bool]
    horizontal_thumbnails: rx.Var[bool]

    # Declarative imperative-control channel (Phase 3): a command object the
    # wrapper applies then clears. Built with helpers in ``commands.py``.
    command: rx.Var[dict[str, Any]]

    # --- Events -------------------------------------------------------------
    # Each forwards the JS callback's first argument to the Python handler.
    on_document_load: rx.EventHandler[lambda num_pages: [num_pages]]
    on_page_change: rx.EventHandler[lambda page: [page]]
    on_scale_change: rx.EventHandler[lambda scale: [scale]]
    on_error: rx.EventHandler[lambda err: [err]]
    on_metadata: rx.EventHandler[lambda meta: [meta]]

    def add_imports(self) -> dict[str, Any]:
        """Import PDFSlick's required stylesheet exactly once."""
        return {"": [PDFSLICK_CSS]}


# Snake_case factory following Reflex convention.
pdf_slick = PdfSlick.create
