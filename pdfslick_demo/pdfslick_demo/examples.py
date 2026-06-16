"""The seven PDFSlick examples reproduced as Reflex pages.

Mirrors ``specs/prd/pdfslick-component.md`` §5. Each builder is a pure function
returning an ``rx.Component`` so it can be unit-tested without a browser and
mounted as a page by the app module.
"""

from __future__ import annotations

import reflex as rx

from reflex_pdfslick import ScaleValue, pdf_slick

from .state import BAD_PDF, SAMPLE_PDF, ErrorState, ViewerState

# (route slug, title, description) — drives the index and page registration.
EXAMPLES: list[tuple[str, str, str]] = [
    ("simple", "Simple Viewer", "Minimal viewer with bottom navigation and zoom."),
    ("full", "Full Viewer App", "Toolbar: zoom, rotation, scroll/spread modes, info."),
    ("thumbnails", "Thumbnails Layout", "A thumbnail sidebar as the primary surface."),
    ("horizontal", "Horizontal Thumbnails", "A horizontal thumbnail strip."),
    ("multiple", "Multiple Documents", "Several independent viewers on one page."),
    ("arraybuffer", "Load from ArrayBuffer", "Open a PDF from an in-memory/remote source."),
    ("error", "Error Handling", "Graceful handling of a load/parse failure."),
]

_FRAME = dict(border="1px solid var(--gray-5)", border_radius="0.5rem", overflow="hidden")


def _nav_bar() -> rx.Component:
    return rx.hstack(
        rx.link("← Gallery", href="/"),
        rx.spacer(),
        rx.text("reflex-pdfslick demo", color_scheme="gray", size="2"),
        width="100%",
        align="center",
        padding_bottom="0.5rem",
    )


def _page(title: str, body: rx.Component) -> rx.Component:
    return rx.container(
        rx.vstack(
            _nav_bar(),
            rx.heading(title, size="6"),
            body,
            spacing="3",
            width="100%",
            padding_y="1.5rem",
        ),
        max_width="1100px",
    )


# 1 — Simple Viewer ---------------------------------------------------------
def simple_viewer() -> rx.Component:
    return _page(
        "Simple Viewer",
        rx.vstack(
            rx.box(
                pdf_slick(
                    url=SAMPLE_PDF,
                    scale_value=ScaleValue.PAGE_WIDTH,
                    on_page_change=ViewerState.on_page_change,
                    on_document_load=ViewerState.on_document_load,
                    height="640px",
                    width="100%",
                ),
                height="640px",
                width="100%",
                position="relative",
                **_FRAME,
            ),
            rx.hstack(
                rx.button("Prev", on_click=ViewerState.go_prev),
                rx.text(f"Page {ViewerState.page_number} / {ViewerState.num_pages}"),
                rx.button("Next", on_click=ViewerState.go_next),
                rx.spacer(),
                rx.button("−", on_click=ViewerState.zoom_out),
                rx.button("+", on_click=ViewerState.zoom_in),
                align="center",
                width="100%",
            ),
            width="100%",
        ),
    )


# 2 — Full Viewer App -------------------------------------------------------
def full_viewer() -> rx.Component:
    toolbar = rx.hstack(
        rx.button("Prev", on_click=ViewerState.go_prev),
        rx.button("Next", on_click=ViewerState.go_next),
        rx.text(f"{ViewerState.page_number}/{ViewerState.num_pages}"),
        rx.divider(orientation="vertical", height="1.5rem"),
        rx.button("−", on_click=ViewerState.zoom_out),
        rx.button("+", on_click=ViewerState.zoom_in),
        rx.select(
            ["auto", "page-actual", "page-fit", "page-width"],
            placeholder="zoom preset",
            on_change=ViewerState.set_preset,
        ),
        rx.divider(orientation="vertical", height="1.5rem"),
        rx.button("⟲", on_click=ViewerState.rotate_ccw),
        rx.button("⟳", on_click=ViewerState.rotate_cw),
        rx.divider(orientation="vertical", height="1.5rem"),
        rx.button("Vert", on_click=ViewerState.scroll_vertical),
        rx.button("Horiz", on_click=ViewerState.scroll_horizontal),
        rx.button("Spread", on_click=ViewerState.spread_odd),
        rx.spacer(),
        rx.button("Print", on_click=ViewerState.print_doc),
        rx.button("Download", on_click=ViewerState.download_doc),
        width="100%",
        align="center",
        wrap="wrap",
        spacing="2",
    )
    return _page(
        "Full Viewer App",
        rx.vstack(
            toolbar,
            rx.cond(
                ViewerState.title != "",
                rx.text(f"Title: {ViewerState.title}", color_scheme="gray", size="2"),
            ),
            rx.box(
                pdf_slick(
                    url=SAMPLE_PDF,
                    scale_value=ScaleValue.PAGE_FIT,
                    command=ViewerState.command,
                    on_page_change=ViewerState.on_page_change,
                    on_document_load=ViewerState.on_document_load,
                    on_scale_change=ViewerState.on_scale_change,
                    on_metadata=ViewerState.on_metadata,
                    height="680px",
                    width="100%",
                ),
                height="680px",
                width="100%",
                position="relative",
                **_FRAME,
            ),
            width="100%",
        ),
    )


# 3 — Thumbnails Layout -----------------------------------------------------
def thumbnails_layout() -> rx.Component:
    return _page(
        "Thumbnails Layout",
        rx.box(
            pdf_slick(
                url=SAMPLE_PDF,
                scale_value=ScaleValue.PAGE_FIT,
                show_thumbnails=True,
                command=ViewerState.command,
                on_page_change=ViewerState.on_page_change,
                on_document_load=ViewerState.on_document_load,
                height="700px",
                width="100%",
            ),
            height="700px",
            width="100%",
            position="relative",
            **_FRAME,
        ),
    )


# 4 — Horizontal Thumbnails -------------------------------------------------
def horizontal_thumbnails() -> rx.Component:
    return _page(
        "Horizontal Thumbnails",
        rx.box(
            pdf_slick(
                url=SAMPLE_PDF,
                scale_value=ScaleValue.PAGE_FIT,
                show_thumbnails=True,
                horizontal_thumbnails=True,
                on_page_change=ViewerState.on_page_change,
                on_document_load=ViewerState.on_document_load,
                height="700px",
                width="100%",
            ),
            height="700px",
            width="100%",
            position="relative",
            **_FRAME,
        ),
    )


# 5 — Multiple Documents ----------------------------------------------------
def multiple_documents() -> rx.Component:
    def one(label: str) -> rx.Component:
        return rx.vstack(
            rx.text(label, weight="bold"),
            rx.box(
                pdf_slick(url=SAMPLE_PDF, scale_value=ScaleValue.PAGE_WIDTH, height="420px", width="100%"),
                height="420px",
                width="100%",
                position="relative",
                **_FRAME,
            ),
            width="100%",
        )

    return _page(
        "Multiple Documents",
        rx.grid(
            one("Document A"),
            one("Document B"),
            columns="2",
            spacing="4",
            width="100%",
        ),
    )


# 6 — Load from ArrayBuffer -------------------------------------------------
def arraybuffer_loader() -> rx.Component:
    # PDFSlick accepts a URL or in-memory bytes. Loading from a remote source
    # exercises the same code path; downstream apps can pass base64/bytes via a
    # data URL or a served asset.
    return _page(
        "Load from ArrayBuffer",
        rx.vstack(
            rx.text(
                "Loads a PDF fetched as bytes. Swap in a data: URL or a served "
                "asset to open in-memory documents.",
                color_scheme="gray",
                size="2",
            ),
            rx.box(
                pdf_slick(
                    url=SAMPLE_PDF,
                    scale_value=ScaleValue.PAGE_FIT,
                    on_document_load=ViewerState.on_document_load,
                    height="640px",
                    width="100%",
                ),
                height="640px",
                width="100%",
                position="relative",
                **_FRAME,
            ),
            width="100%",
        ),
    )


# 7 — Error Handling --------------------------------------------------------
def error_handling() -> rx.Component:
    return _page(
        "Error Handling",
        rx.vstack(
            rx.cond(
                ErrorState.has_error,
                rx.callout(
                    f"Could not load PDF: {ErrorState.error_message}",
                    icon="triangle_alert",
                    color_scheme="red",
                ),
                rx.text("Attempting to load a non-existent PDF…", color_scheme="gray"),
            ),
            rx.box(
                pdf_slick(
                    url=BAD_PDF,
                    on_error=ErrorState.on_error,
                    height="400px",
                    width="100%",
                ),
                height="400px",
                width="100%",
                position="relative",
                **_FRAME,
            ),
            width="100%",
        ),
    )


def _card(slug: str, title: str, desc: str) -> rx.Component:
    return rx.link(
        rx.box(
            rx.heading(title, size="4"),
            rx.text(desc, color_scheme="gray", size="2"),
            padding="1rem",
            border="1px solid var(--gray-5)",
            border_radius="0.5rem",
            width="100%",
            _hover={"border_color": "var(--accent-8)"},
        ),
        href=f"/{slug}",
        width="100%",
    )


def index() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading("reflex-pdfslick — Example Gallery", size="7"),
            rx.text(
                "Native Reflex wrapper for PDFSlick (PDF.js + Zustand). "
                "Seven examples reproducing the PDFSlick gallery.",
            ),
            rx.divider(),
            rx.grid(
                *[_card(slug, title, desc) for slug, title, desc in EXAMPLES],
                columns="2",
                spacing="3",
                width="100%",
            ),
            spacing="4",
            padding_y="2rem",
            width="100%",
        ),
        max_width="1000px",
    )
