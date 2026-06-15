"""Typed PDFSlick options object.

Mirrors the ``PDFSlickOptions`` type from ``@pdfslick/core@4.x``. Subclassing
``rx.PropsBase`` means snake_case Python fields are auto-converted to the
camelCase keys PDFSlick expects when serialized to a JS object prop.

Only the most commonly used options are surfaced as first-class fields; the full
upstream option set is documented in ``specs/api/component-api.md``. Unknown or
advanced keys can still be passed through ``extra``.
"""

from __future__ import annotations

from typing import Any, Optional

import reflex as rx


class PdfSlickOptions(rx.PropsBase):
    """Options forwarded to ``usePDFSlick(url, options)``.

    Field names are snake_case in Python and emitted as camelCase to JS, e.g.
    ``single_page_viewer`` -> ``singlePageViewer``.
    """

    scale_value: Optional[str] = None  # "auto" | "page-fit" | "page-width" | "page-actual" | numeric
    single_page_viewer: Optional[bool] = None
    remove_page_borders: Optional[bool] = None
    enable_print_auto_rotate: Optional[bool] = None
    use_only_css_zoom: Optional[bool] = None
    text_layer_mode: Optional[int] = None
    annotation_mode: Optional[int] = None
    annotation_editor_mode: Optional[int] = None
    thumbnail_width: Optional[int] = None
    print_resolution: Optional[int] = None
    max_canvas_pixels: Optional[int] = None
    filename: Optional[str] = None

    # Escape hatch for advanced/less-common upstream options (e.g.
    # ``getDocumentParams``). Merged verbatim into the JS options object.
    extra: dict[str, Any] = {}
