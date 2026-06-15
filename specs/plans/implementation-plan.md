# reflex-pdfslick — Implementation Plan

## Metadata

| Field | Value |
|---|---|
| **Author** | Ernesto Crespo |
| **Status** | `IN PROGRESS` |
| **Version** | 1.0 |
| **Date** | 2026-06-15 |
| **PRD** | `../prd/pdfslick-component.md` |
| **Tech Design** | `../technical/architecture.md` |
| **Data Model** | `../data-model/store-schema.md` |
| **API Spec** | `../api/component-api.md` |
| **Tasks** | `../tasks/task-breakdown.md` |

---

## 1. Summary

Build a native Reflex component wrapping `@pdfslick/react`, plus a demo app that
reproduces PDFSlick's example gallery. Delivery is **phased** and
**test-driven**: the Python layer (options, enums, serialization) is tested
without a running frontend; integration is validated in the demo build.

**Team:** 1 developer. **Method:** spec-first, then incremental phases.

## 2. Pre-requisites

| Pre-requisite | Owner | Status |
|---|---|---|
| Research PDFSlick API, store, examples, versions | Ernesto | ☑ (see `../research/`) |
| Research Reflex custom-component / NoSSR / hook wrapping | Ernesto | ☑ (see `../research/`) |
| Confirm `@pdfslick/react@4.0.0` + `pdfjs-dist@^6.0.227` | Ernesto | ☑ |

## 3. Phases

### Phase 0 — Foundation & SDD  ✅ *(current commit)*

**Objective:** repository, packaging, and the full SDD documentation set.

| Done when |
|---|
| Repo scaffolded (`custom_components/`, `specs/`, `tests/`, `pdfslick_demo/`). |
| `pyproject.toml`, `.gitignore`, `LICENSE`, `README.md` present. |
| PRD, technical, API, data-model, plan, tasks, research docs written. |
| Package imports cleanly (`import reflex_pdfslick`). |

### Phase 1 — Core wrapper

**Objective:** a working viewer from a `url`.

| Deliverable |
|---|
| `js/PdfSlickWrapper.tsx` calling `usePDFSlick`, rendering `<PDFSlickViewer>`. |
| `PdfSlick(rx.NoSSRComponent)` wired via `rx.asset` + `$/public` library path. |
| CSS imported via `add_imports`; npm dep pinned in `lib_dependencies`. |
| Props: `url`, `scale_value`, `single_page_viewer`, `remove_page_borders`. |
| Demo "Simple Viewer" screen renders a PDF; PDF.js worker resolves in build. |

**Exit:** the demo loads and displays a PDF without SSR errors.

### Phase 2 — Events & state bridge

**Objective:** viewer state flows into Reflex.

| Deliverable |
|---|
| Store subscriptions for `pageNumber`, `numPages`, `scale`, `isDocumentLoaded`, `error`. |
| Events `on_document_load`, `on_page_change`, `on_scale_change`, `on_error`. |
| Date/Map normalization rules applied for any metadata emitted. |
| Demo shows live page/total/scale bound to Reflex state. |

**Exit:** changing pages/zoom updates Python state; errors surface to `on_error`.

### Phase 3 — Imperative controls

**Objective:** drive the viewer from Python.

| Deliverable |
|---|
| Declarative `command` prop + wrapper handler (apply-then-clear). |
| Controls: goto/next/prev, zoom in/out, zoom preset, zoom value, rotate. |
| Scroll/spread modes via `ScrollMode`/`SpreadMode`. |
| Print (`triggerPrinting`) and download/save (`downloadOrSave`). |
| Demo "Full Viewer App" toolbar wired to controls. |

**Exit:** a Python toolbar fully controls the viewer.

### Phase 4 — Thumbnails & multi-document

**Objective:** thumbnails and multiple instances.

| Deliverable |
|---|
| `show_thumbnails` sidebar (fixed layout, click → goto page). |
| Horizontal thumbnail variant. |
| Verified independent multi-instance usage (separate stores). |
| Demo "Thumbnails Layout", "Horizontal Thumbnails", "Multiple Documents". |

**Exit:** thumbnails navigate; multiple viewers coexist on one page.

### Phase 5 — Demo gallery & docs polish

**Objective:** complete the example set and ArrayBuffer loading.

| Deliverable |
|---|
| "Load from ArrayBuffer" (bytes/base64) example. |
| "Error Handling" example. |
| Demo navigation/index across all 7 examples. |
| README usage docs finalized; per-example notes. |

**Exit:** all 7 examples runnable from the demo.

### Phase 6 — Tests, CI & release

**Objective:** quality gates and PyPI.

| Deliverable |
|---|
| Python unit tests (enums, options serialization, imports, prop/event surface). |
| GitHub Actions: lint + pytest + demo build smoke test. |
| `reflex component build`; publish to PyPI (`twine`/`uv`). |
| Tagged GitHub release; README badges live. |

**Exit:** green CI; `pip install reflex-pdfslick` works.

## 4. Sequencing & dependencies

```
Phase 0 ──► Phase 1 ──► Phase 2 ──► Phase 3 ──► Phase 4 ──► Phase 5 ──► Phase 6
 (SDD)      (viewer)    (events)   (controls)  (thumbs)   (gallery)   (release)
```

Phases 2 and 3 can partially overlap once Phase 1 stabilizes the wrapper.

## 5. Risks & mitigations (delivery)

| Risk | Mitigation |
|---|---|
| PDF.js worker mismatch in Reflex bundler | Validate in Phase 1 demo build; document `workerSrc` override. |
| ESM-only pdf.js v6 bundling | Keep wrapper minimal; test build early. |
| Reflex API drift across 0.9.x | Pin a known-good Reflex range in demo `requirements.txt`. |

## 6. Definition of Done (project)

- All 7 examples run in the demo.
- Events and imperative controls behave per the API spec.
- Tests pass in CI; package published to PyPI; release tagged.
- Documentation (`specs/`, README) consistent with shipped behavior.
