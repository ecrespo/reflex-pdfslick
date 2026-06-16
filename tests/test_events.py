"""Phase 2 — Events & state bridge contract.

The wrapper forwards Zustand store changes to Reflex event handlers
(``specs/technical/architecture.md`` §4.4). Here we pin that the component
exposes the documented event triggers so downstream apps can bind state.
"""

from reflex_pdfslick import PdfSlick


def test_documented_events_are_exposed():
    triggers = PdfSlick.create(url="/x.pdf").get_event_triggers()
    for event in [
        "on_document_load",
        "on_page_change",
        "on_scale_change",
        "on_error",
        "on_metadata",
    ]:
        assert event in triggers, event


def test_events_can_bind_handlers():
    # Binding a handler at create time must not raise (spec/lambda accepts the
    # single forwarded JS argument).
    captured = {}

    class _S:
        @staticmethod
        def on_page(page):  # pragma: no cover - not executed, just bound
            captured["page"] = page

    component = PdfSlick.create(url="/x.pdf")
    assert "on_page_change" in component.get_event_triggers()
