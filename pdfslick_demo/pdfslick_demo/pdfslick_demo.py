"""reflex-pdfslick demo app (skeleton).

This is the Phase-0 skeleton for the example gallery described in
``specs/prd/pdfslick-component.md`` (§5) and ``specs/tasks/task-breakdown.md``.
Each example screen is filled in across Phases 1–5 as the component runtime is
implemented. For now it renders an index of the planned examples so the demo
app is runnable and self-describing.

Once Phase 1 lands, replace ``_placeholder`` usages with real ``pdf_slick(...)``
viewers, e.g.::

    from reflex_pdfslick import pdf_slick, ScaleValue

    def simple_viewer():
        return pdf_slick(url="/sample.pdf", scale_value=ScaleValue.PAGE_FIT,
                         height="700px")
"""

import reflex as rx

EXAMPLES = [
    ("Simple Viewer", "Basic viewer with prev/next navigation and zoom."),
    ("Full Viewer App", "Toolbar, zoom, rotation, scroll/spread modes, info, search, thumbnails."),
    ("Thumbnails Layout", "A grid of page thumbnails as the primary surface."),
    ("Horizontal Thumbnails", "A horizontal thumbnail strip."),
    ("Multiple Documents", "Several independent viewers on one page."),
    ("Load from ArrayBuffer", "Open a PDF from in-memory bytes."),
    ("Error Handling", "Graceful handling of load/parse errors."),
]


def _card(title: str, desc: str) -> rx.Component:
    return rx.box(
        rx.heading(title, size="4"),
        rx.text(desc, color_scheme="gray"),
        rx.badge("planned", color_scheme="amber"),
        padding="1rem",
        border="1px solid var(--gray-5)",
        border_radius="0.5rem",
        width="100%",
    )


def index() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading("reflex-pdfslick — Example Gallery", size="7"),
            rx.text(
                "Native Reflex wrapper for PDFSlick (PDF.js + Zustand). "
                "Examples are implemented per the SDD plan in specs/.",
            ),
            rx.divider(),
            rx.vstack(
                *[_card(t, d) for t, d in EXAMPLES],
                spacing="3",
                width="100%",
            ),
            spacing="4",
            padding_y="2rem",
            width="100%",
        ),
    )


app = rx.App()
app.add_page(index, title="reflex-pdfslick demo")
