# reflex-pdfslick

[![PyPI version](https://img.shields.io/pypi/v/reflex-pdfslick.svg)](https://pypi.org/project/reflex-pdfslick/)
[![Python versions](https://img.shields.io/pypi/pyversions/reflex-pdfslick.svg)](https://pypi.org/project/reflex-pdfslick/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/ecrespo/reflex-pdfslick/blob/main/LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-ecrespo%2Freflex--pdfslick-181717?logo=github)](https://github.com/ecrespo/reflex-pdfslick)

- **Source:** https://github.com/ecrespo/reflex-pdfslick
- **Issues:** https://github.com/ecrespo/reflex-pdfslick/issues
- **PDFSlick (upstream):** https://github.com/pdfslick/pdfslick — https://pdfslick.dev

A native [Reflex](https://reflex.dev/) component that wraps
[**PDFSlick**](https://pdfslick.dev/) so you can view and interact with PDF
documents in **pure Python** — no HTML, no `iframe`, no hand-written
JavaScript.

PDFSlick is built on top of Mozilla's [PDF.js](https://github.com/mozilla/pdf.js)
and uses [Zustand](https://github.com/pmndrs/zustand) to expose a reactive store
for the loaded document. `reflex-pdfslick` bridges that store and PDFSlick's
imperative API into Reflex's declarative, state-driven model: document state
(page number, page count, zoom, rotation, metadata, thumbnails) flows back to
Python as events, and Python triggers actions (go to page, zoom, rotate, print,
download) on the viewer.

> **Project status — `ALPHA` / specification-first.**
> This repository currently contains the full **Spec-Driven Design (SDD)**
> documentation set, the package scaffold, and the demo-app skeleton. The
> component runtime and the example gallery are delivered incrementally per the
> [implementation plan](specs/plans/implementation-plan.md). See
> [Roadmap](#roadmap) for what is and isn't built yet.

```python
import reflex as rx
from reflex_pdfslick import pdf_slick


class State(rx.State):
    page_number: int = 1
    num_pages: int = 0

    @rx.event
    def on_page_change(self, page: int):
        self.page_number = page

    @rx.event
    def on_document_load(self, num_pages: int):
        self.num_pages = num_pages


def index() -> rx.Component:
    return pdf_slick(
        url="/sample.pdf",
        scale_value="page-fit",
        single_page_viewer=True,
        on_page_change=State.on_page_change,
        on_document_load=State.on_document_load,
        height="700px",
    )


app = rx.App()
app.add_page(index)
```

## Why a native component instead of an `iframe`?

Embedding a PDF viewer through an `iframe` or a raw `<embed>` works, but it is
isolated from your app: you cannot react to page changes, drive the zoom from a
Python toolbar, or read the document's metadata into your state. Wrapping
PDFSlick as a first-class Reflex component means:

- **Reactive state** — `page_number`, `num_pages`, `scale`, `rotation`,
  `is_document_loaded` and document metadata are pushed into Reflex state via
  typed events.
- **Imperative control from Python** — go to page, zoom in/out, fit width/page,
  rotate, switch scroll/spread modes, print and download are exposed as
  component-level controls.
- **Reusable & versioned** — installable with `pip`, with the npm dependency
  (`@pdfslick/react`) pinned for reproducible builds.
- **SSR-safe** — PDF.js is browser-only, so the component is wrapped as a
  Reflex `NoSSRComponent` and only ever renders on the client.

## Installation

```shell
pip install reflex-pdfslick
# or, from source
git clone https://github.com/ecrespo/reflex-pdfslick.git
cd reflex-pdfslick
pip install -e .
```

Reflex installs the underlying npm packages automatically on first run. The
component pins `@pdfslick/react` (which pulls in `@pdfslick/core`, `pdfjs-dist`
and `zustand`) and imports the required stylesheet
`@pdfslick/react/dist/pdf_viewer.css` for you.

## Planned API (summary)

The full contract lives in [specs/api/component-api.md](specs/api/component-api.md).

| Prop | Type | Description |
|---|---|---|
| `url` | `str` | Path/URL of the PDF to load. |
| `scale_value` | `str` | `"auto"`, `"page-fit"`, `"page-width"`, `"page-actual"` or a numeric string. |
| `single_page_viewer` | `bool` | Render a single page at a time. |
| `thumbnail_width` | `int` | Width (px) of generated thumbnails. |
| `remove_page_borders` | `bool` | Hide page borders. |

| Event | Payload | Fired when |
|---|---|---|
| `on_document_load` | `int` (num pages) | The document finishes loading. |
| `on_page_change` | `int` (page) | The current page changes. |
| `on_scale_change` | `float` (scale) | The zoom level changes. |
| `on_error` | `dict` | Loading/parsing fails. |

Imperative controls (next/previous page, zoom, rotate, print, download) are
driven from Python state — see the API spec for the dispatch mechanism.

## Examples (demo gallery)

The `pdfslick_demo/` Reflex app mirrors PDFSlick's own example set. Each example
is documented in the [PRD](specs/prd/pdfslick-component.md) and
[task breakdown](specs/tasks/task-breakdown.md):

1. **Simple Viewer** — basic viewer with prev/next navigation and zoom.
2. **Full Viewer App** — toolbar, zoom selector, rotation, scroll/spread modes,
   document info, search and thumbnails sidebar.
3. **Thumbnails Layout** — a grid of page thumbnails as the primary surface.
4. **Horizontal Thumbnails** — a horizontal thumbnail strip.
5. **Multiple Documents** — several independent viewers on one page.
6. **Load from ArrayBuffer** — open a PDF from in-memory bytes.
7. **Error Handling** — graceful handling of load/parse errors.

Run the demo:

```shell
cd pdfslick_demo
pip install -r requirements.txt
reflex run
```

## Architecture (at a glance)

```
Python (Reflex app)
  pdf_slick(url=..., scale_value=..., on_page_change=...)
        │  compiles to
        ▼
React / Next.js (generated by Reflex)
  <PdfSlickWrapper>  ← local .tsx, NoSSR, calls usePDFSlick(url, options)
        │  renders <PDFSlickViewer/> + (optional) thumbnails
        │  subscribes to usePDFSlickStore selectors → emits Reflex events
        ▼
@pdfslick/react → @pdfslick/core → PDF.js (pdfjs-dist) + Zustand store
```

Because PDFSlick's public surface is the **hook** `usePDFSlick(...)` (not a
drop-in component) and its thumbnails component uses a render-prop child, the
wrapper is a small local `.tsx` component that calls the hook internally and
exposes a clean prop/event API to Python. Full rationale and trade-offs are in
[specs/technical/architecture.md](specs/technical/architecture.md).

## Spec-Driven Design documentation

This project is documented before it is built. The `specs/` directory is the
source of truth:

| Document | Purpose |
|---|---|
| [`specs/prd/pdfslick-component.md`](specs/prd/pdfslick-component.md) | Product requirements, goals, scope, examples. |
| [`specs/technical/architecture.md`](specs/technical/architecture.md) | Technical design, SSR strategy, wrapper pattern. |
| [`specs/api/component-api.md`](specs/api/component-api.md) | Public Python API: props, events, controls. |
| [`specs/data-model/store-schema.md`](specs/data-model/store-schema.md) | PDFSlick store schema and Python ↔ JS mapping. |
| [`specs/plans/implementation-plan.md`](specs/plans/implementation-plan.md) | Phases, milestones, sequencing. |
| [`specs/tasks/task-breakdown.md`](specs/tasks/task-breakdown.md) | Granular, trackable task list per phase. |
| [`specs/research/pdfslick-and-reflex-research.md`](specs/research/pdfslick-and-reflex-research.md) | Primary-source research notes that ground the design. |

## Roadmap

- [x] **Phase 0 — Foundation & SDD** *(this commit)*: repository, packaging,
      SDD artifacts, README, demo skeleton.
- [ ] **Phase 1 — Core wrapper**: `PdfSlickWrapper.tsx`, `pdf_slick` component,
      props, CSS import, NoSSR.
- [ ] **Phase 2 — Events & state bridge**: page/scale/load/error events.
- [ ] **Phase 3 — Imperative controls**: navigation, zoom, rotation, modes,
      print, download.
- [ ] **Phase 4 — Thumbnails & multi-document**.
- [ ] **Phase 5 — Demo gallery** (all examples) **& docs polish**.
- [ ] **Phase 6 — Tests, CI, PyPI release**.

## Credits

- [PDFSlick](https://pdfslick.dev/) by
  [Vancho Stojkov](https://github.com/van100j) — the library being wrapped (MIT).
- [PDF.js](https://github.com/mozilla/pdf.js) by Mozilla.
- [Reflex](https://reflex.dev/) — the Python web framework.

This wrapper is an independent project and is not affiliated with or endorsed by
the PDFSlick authors.

## License

[MIT](LICENSE) © Ernesto Crespo
