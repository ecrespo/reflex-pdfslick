"""Phase 5 — Demo gallery example builders.

Each of PDFSlick's seven reproduced examples is a pure builder function that
returns an ``rx.Component`` (``specs/prd/pdfslick-component.md`` §5). Testing
that they construct without error guards the demo against API drift in the
component, without needing a browser.
"""

import reflex as rx

from pdfslick_demo import examples


EXAMPLE_BUILDERS = [
    "simple_viewer",
    "full_viewer",
    "thumbnails_layout",
    "horizontal_thumbnails",
    "multiple_documents",
    "arraybuffer_loader",
    "error_handling",
]


def test_all_seven_builders_exist():
    for name in EXAMPLE_BUILDERS:
        assert hasattr(examples, name), name


def test_each_builder_returns_a_component():
    for name in EXAMPLE_BUILDERS:
        component = getattr(examples, name)()
        assert isinstance(component, rx.Component), name


def test_index_lists_seven_examples():
    assert len(examples.EXAMPLES) == 7
    assert isinstance(examples.index(), rx.Component)


def test_app_module_imports_and_registers_pages():
    # Importing the app module must wire all example pages without error.
    from pdfslick_demo import pdfslick_demo as app_module

    assert isinstance(app_module.app, rx.App)
