"""reflex-pdfslick demo app — the PDFSlick example gallery.

Reproduces the seven examples from ``specs/prd/pdfslick-component.md`` §5. The
index lists them; each example is its own route. The builder functions live in
``examples.py`` so they can be unit-tested without a browser.
"""

import reflex as rx

from . import examples

# Map example slugs to their builder functions.
_BUILDERS = {
    "simple": examples.simple_viewer,
    "full": examples.full_viewer,
    "thumbnails": examples.thumbnails_layout,
    "horizontal": examples.horizontal_thumbnails,
    "multiple": examples.multiple_documents,
    "arraybuffer": examples.arraybuffer_loader,
    "error": examples.error_handling,
}

app = rx.App()
app.add_page(examples.index, route="/", title="reflex-pdfslick demo")

for _slug, _title, _desc in examples.EXAMPLES:
    app.add_page(
        _BUILDERS[_slug],
        route=f"/{_slug}",
        title=f"{_title} — reflex-pdfslick",
    )
