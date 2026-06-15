# reflex-pdfslick — Native PDFSlick Component

## Product Requirements Document (PRD)

| Field | Value |
|---|---|
| **Author** | Ernesto Crespo |
| **Status** | `APPROVED` |
| **Version** | 1.0 |
| **Date** | 2026-06-15 |
| **Reviewers** | — |
| **Last updated** | 2026-06-15 |

---

## 1. Executive Summary

`reflex-pdfslick` is a pip-installable [Reflex](https://reflex.dev/) component
that natively wraps [**PDFSlick**](https://pdfslick.dev/), a PDF viewing and
interaction library built on Mozilla's [PDF.js](https://github.com/mozilla/pdf.js)
with a [Zustand](https://github.com/pmndrs/zustand) reactive store. It lets a
Reflex developer embed a fully interactive PDF viewer — navigation, zoom,
rotation, scroll/spread modes, thumbnails, document metadata, printing and
downloading — declared in **pure Python**, with viewer state flowing into Reflex
state and Python driving viewer actions.

The product packages PDFSlick's React surface (`@pdfslick/react`) as a
first-class, version-pinned, SSR-safe Reflex component, plus a demo application
that reproduces PDFSlick's own example gallery.

## 2. Context and Problem

### 2.1 Current Situation

Reflex has no native, reactive PDF viewer. Developers fall back to one of:

1. An `<iframe>` / `<embed>` pointing at a static file or the browser's built-in
   PDF plugin.
2. Hand-wiring PDF.js or a React PDF library through ad-hoc custom code per
   project.

PDFSlick already solves the hard part on the JS side — it wraps PDF.js into a
React-friendly hook (`usePDFSlick`) plus a reactive store — but it is not
consumable from Python/Reflex.

### 2.2 Problem

1. **No reactivity** — an `iframe`/`embed` viewer cannot communicate with Reflex
   state; you cannot react to page changes, drive zoom from a Python toolbar, or
   read the document's metadata into your app.
2. **Not reusable** — per-project custom code is duplicated and brittle.
3. **SSR hazards** — PDF.js touches `window`/`document` and breaks Reflex's
   server-side render unless explicitly deferred to the client.
4. **No typing** — option/enum values (scroll modes, spread modes, scale
   presets) are magic numbers/strings that are easy to get wrong.

### 2.3 Opportunity

Package PDFSlick as a native Reflex component — version-pinned via npm, with
typed options/enums in Python and events bound to state — benefiting any Reflex
developer who needs to display or interact with PDFs.

## 3. Target Users

### Persona 1: Reflex Developer
- **Description:** builds full-stack Python apps with Reflex.
- **Primary need:** drop an interactive PDF viewer into a page with a few lines,
  without writing JS.
- **Usage frequency:** per project / per feature.
- **Technical level:** medium/high.

### Persona 2: Document-heavy app builder
- **Description:** builds apps where PDFs are central (invoices, contracts,
  reports, manuals, e-readers).
- **Primary need:** navigation, thumbnails, search, zoom, print/download, and
  reading viewer state (current page, total pages, metadata) into app logic.
- **Usage frequency:** continuous.
- **Technical level:** medium.

## 4. Goals and Success Metrics

| Goal | Metric | Target |
|---|---|---|
| Easy embedding | Lines of Python to render a working viewer | ≤ 5 |
| Reactivity | Viewer events bound to Reflex state | page, scale, load, error |
| Control | Imperative actions callable from Python | nav, zoom, rotate, modes, print, download |
| Stability | npm dependency pinned | `@pdfslick/react@4.0.0` |
| SSR safety | Server render crashes | 0 |
| Coverage | PDFSlick examples reproduced in demo | 7/7 |

### Non-goals (v1)

- Editing/annotating PDFs and persisting annotations (PDFSlick exposes
  annotation-editor modes; a Python-level annotation API is **out of scope** for
  v1 and tracked as a future enhancement).
- A render-prop thumbnail API exposed to Python (thumbnails are rendered inside
  the JS wrapper with a fixed layout; custom per-thumbnail Python rendering is
  out of scope).
- Server-side PDF generation or manipulation.

## 5. Scope — Examples to Reproduce

The demo gallery mirrors PDFSlick's published examples. Each maps to features
the component must support:

| # | Example | Demonstrates | Key features used |
|---|---|---|---|
| 1 | **Simple Viewer** | Minimal viewer + bottom nav | `gotoPage`, zoom in/out, `pageNumber`, `numPages`, `scale` |
| 2 | **Full Viewer App** | Toolbar, zoom selector, rotation, modes, info, search, thumbnails | `currentScale`/`currentScaleValue`, `setRotation`, `setScrollMode`, `setSpreadMode`, metadata, `triggerPrinting`, `downloadOrSave` |
| 3 | **Thumbnails Layout** | Thumbnail grid as primary surface | `thumbnails` store map, `gotoPage` |
| 4 | **Horizontal Thumbnails** | Horizontal thumbnail strip | thumbnails + `setScrollMode` |
| 5 | **Multiple Documents** | Several independent viewers on one page | independent `usePDFSlick` instances/stores |
| 6 | **Load from ArrayBuffer** | Open a PDF from in-memory bytes | `loadDocument(arrayBuffer)` |
| 7 | **Error Handling** | Graceful load/parse failure | `error` from `usePDFSlick` |

## 6. Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| FR-01 | Render a PDF from a URL/path via a `url` prop. | P0 |
| FR-02 | Configure initial zoom via `scale_value` (presets + numeric). | P0 |
| FR-03 | Single-page vs continuous viewing via `single_page_viewer`. | P0 |
| FR-04 | Emit `on_document_load(num_pages)` when loaded. | P0 |
| FR-05 | Emit `on_page_change(page)` on page change. | P0 |
| FR-06 | Emit `on_scale_change(scale)` on zoom change. | P1 |
| FR-07 | Emit `on_error(err)` on failure. | P0 |
| FR-08 | Imperative controls from Python: go to page, next/prev, zoom in/out, fit width/page, rotate, scroll mode, spread mode. | P1 |
| FR-09 | Print and download/save from Python. | P1 |
| FR-10 | Optional thumbnails sidebar via `show_thumbnails`. | P1 |
| FR-11 | Expose document metadata (title, author, page count, etc.) to state. | P2 |
| FR-12 | Support multiple independent instances on one page. | P1 |
| FR-13 | Load from in-memory bytes (ArrayBuffer / base64). | P2 |

## 7. Non-Functional Requirements

- **SSR-safe:** never access `window` during server render (NoSSR).
- **Reproducible:** npm dependency pinned; CSS imported once.
- **Typed:** enums (`ScrollMode`, `SpreadMode`, `ScaleValue`) and `PdfSlickOptions`.
- **Maintainable:** thin JS wrapper; Python layer testable in isolation.
- **Documented:** SDD specs are the source of truth; README usage examples.
- **Licensed:** MIT, consistent with PDFSlick and PDF.js.

## 8. Constraints & Dependencies

- `@pdfslick/react@4.0.0` → `@pdfslick/core@4.0.0` → `pdfjs-dist@^6.0.227`,
  `zustand@^5`. React peer `>=17`.
- Reflex `>=0.9.0` (current line; component-wrapping + `NoSSRComponent` API).
- The PDF.js worker version must match the bundled `pdfjs-dist` version.

## 9. Risks

| Risk | Impact | Mitigation |
|---|---|---|
| PDF.js worker version mismatch under Reflex's bundler | Viewer fails to init | Pin `@pdfslick/react`; verify worker bundling in Phase 1; document override |
| `<PDFSlickThumbnails>` render-prop not expressible from Python | Limited thumbnail customization | Render thumbnails inside the JS wrapper with a fixed layout |
| Non-serializable store fields (`Map`, `Date`, class instances) | Cannot sync directly to Python | Bridge only serializable scalars; convert dates/maps in the wrapper |
| ESM-only pdf.js v6 bundling issues | Build breaks | Validate in demo build; keep wrapper minimal |

## 10. Acceptance Criteria

- A Reflex page renders a working PDF viewer from a `url` in ≤ 5 lines.
- Page changes and document load update Reflex state via events.
- Python can drive navigation and zoom.
- The demo app builds and runs all 7 example screens.
- No SSR crash; npm dependency pinned; MIT license present.
