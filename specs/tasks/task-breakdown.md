# reflex-pdfslick — Task Breakdown

## Metadata

| Field | Value |
|---|---|
| **Author** | Ernesto Crespo |
| **Status** | `COMPLETE` |
| **Version** | 1.0 |
| **Date** | 2026-06-15 |
| **Plan** | `../plans/implementation-plan.md` |

Legend: ☑ done · ☐ pending · ◐ in progress

---

## Phase 0 — Foundation & SDD

| ID | Task | Est. | Dep. | Status |
|---|---|---|---|---|
| F0-01 | Init git repo on `main`, author config | 0.1h | — | ☑ |
| F0-02 | Directory layout (`custom_components/`, `specs/`, `tests/`, `pdfslick_demo/`) | 0.25h | F0-01 | ☑ |
| F0-03 | `pyproject.toml` (pip package + pytest config) | 0.25h | F0-02 | ☑ |
| F0-04 | `.gitignore`, `LICENSE` (MIT) | 0.1h | F0-02 | ☑ |
| F0-05 | `README.md` (overview, install, API summary, roadmap) | 0.5h | F0-03 | ☑ |
| F0-06 | Package scaffold: `__init__.py`, `models.py`, `options.py`, `pdfslick.py` | 0.5h | F0-03 | ☑ |
| F0-07 | `js/PdfSlickWrapper.tsx` reference artifact | 0.3h | F0-06 | ☑ |
| F0-08 | SDD: PRD | 0.5h | — | ☑ |
| F0-09 | SDD: technical/architecture | 0.5h | F0-08 | ☑ |
| F0-10 | SDD: API spec | 0.4h | F0-08 | ☑ |
| F0-11 | SDD: data-model/store schema | 0.4h | F0-08 | ☑ |
| F0-12 | SDD: implementation plan (phases) | 0.3h | F0-08 | ☑ |
| F0-13 | SDD: task breakdown (this doc) | 0.2h | F0-12 | ☑ |
| F0-14 | SDD: research notes | 0.3h | — | ☑ |
| F0-15 | Demo skeleton (`rxconfig.py`, requirements, app module) | 0.3h | F0-02 | ☑ |
| F0-16 | Smoke test: `import reflex_pdfslick` | 0.1h | F0-06 | ☑ |

**Done:** repo imports cleanly; all SDD docs present and cross-linked.

## Phase 1 — Core wrapper

| ID | Task | Est. | Dep. | Status |
|---|---|---|---|---|
| F1-01 | Finalize `PdfSlickWrapper.tsx` (hook, viewer, CSS import) | 1h | F0-07 | ☑ |
| F1-02 | Wire `PdfSlick(rx.NoSSRComponent)` via `rx.asset` + `$/public` | 1h | F1-01 | ☑ |
| F1-03 | `lib_dependencies = ["@pdfslick/react@4.0.0"]`; CSS in `add_imports` | 0.25h | F1-02 | ☑ |
| F1-04 | Props: `url`, `scale_value`, `single_page_viewer`, `remove_page_borders` | 0.5h | F1-02 | ☑ |
| F1-05 | Verify PDF.js worker bundling in demo build | 1h | F1-04 | ☑ |
| F1-06 | Demo "Simple Viewer" renders a sample PDF | 0.5h | F1-05 | ☑ |

**Done:** demo loads & displays a PDF, no SSR error.

## Phase 2 — Events & state bridge

| ID | Task | Est. | Dep. | Status |
|---|---|---|---|---|
| F2-01 | Store selectors: `pageNumber`, `numPages`, `scale`, `isDocumentLoaded`, `error` | 0.5h | F1-06 | ☑ |
| F2-02 | Events `on_document_load`, `on_page_change` | 0.5h | F2-01 | ☑ |
| F2-03 | Events `on_scale_change`, `on_error` | 0.5h | F2-01 | ☑ |
| F2-04 | Date/Map normalization helpers in wrapper | 0.5h | F2-01 | ☑ |
| F2-05 | Demo: live page/total/scale bound to state | 0.5h | F2-02 | ☑ |

**Done:** page/zoom changes update Python state; errors surface.

## Phase 3 — Imperative controls

| ID | Task | Est. | Dep. | Status |
|---|---|---|---|---|
| F3-01 | `command` prop + apply-then-clear handler | 1h | F2-05 | ☑ |
| F3-02 | Nav: goto / next / prev | 0.5h | F3-01 | ☑ |
| F3-03 | Zoom: in/out, preset, value (`currentScale`/`currentScaleValue`) | 0.5h | F3-01 | ☑ |
| F3-04 | Rotation (`setRotation`) | 0.25h | F3-01 | ☑ |
| F3-05 | Scroll/spread modes (`setScrollMode`/`setSpreadMode`) | 0.5h | F3-01 | ☑ |
| F3-06 | Print (`triggerPrinting`), download/save (`downloadOrSave`) | 0.5h | F3-01 | ☑ |
| F3-07 | Demo "Full Viewer App" toolbar | 1.5h | F3-02..06 | ☑ |

**Done:** a Python toolbar fully controls the viewer.

## Phase 4 — Thumbnails & multi-document

| ID | Task | Est. | Dep. | Status |
|---|---|---|---|---|
| F4-01 | `show_thumbnails` sidebar (click → goto page) | 1h | F3-07 | ☑ |
| F4-02 | Horizontal thumbnails variant | 0.5h | F4-01 | ☑ |
| F4-03 | Verify multi-instance (separate stores) | 0.5h | F1-06 | ☑ |
| F4-04 | Demo: Thumbnails Layout / Horizontal / Multiple Documents | 1.5h | F4-01..03 | ☑ |

**Done:** thumbnails navigate; multiple viewers coexist.

## Phase 5 — Demo gallery & docs polish

| ID | Task | Est. | Dep. | Status |
|---|---|---|---|---|
| F5-01 | ArrayBuffer/base64 loading example | 1h | F2-05 | ☑ |
| F5-02 | Error-handling example | 0.5h | F2-03 | ☑ |
| F5-03 | Demo index/navigation across 7 examples | 0.5h | F4-04 | ☑ |
| F5-04 | README usage finalization + per-example notes | 0.5h | F5-03 | ☑ |

**Done:** all 7 examples runnable.

## Phase 6 — Tests, CI & release

| ID | Task | Est. | Dep. | Status |
|---|---|---|---|---|
| F6-01 | Unit tests: enums values | 0.25h | F0-06 | ☑ |
| F6-02 | Unit tests: `PdfSlickOptions` snake→camel serialization | 0.5h | F0-06 | ☑ |
| F6-03 | Unit tests: import surface + prop/event presence | 0.5h | F1-04 | ☑ |
| F6-04 | GitHub Actions: lint + pytest + demo build smoke | 1h | F6-03 | ☑ |
| F6-05 | `reflex component build` + PyPI publish | 0.5h | F6-04 | ☐ (needs maintainer PyPI credentials) |
| F6-06 | Tag GitHub release; verify badges | 0.25h | F6-05 | ☐ (needs maintainer release access) |

**Done (engineering):** green CI; demo compiles to a Reflex production build.
**Remaining (release):** F6-05/F6-06 require maintainer credentials (PyPI token,
GitHub release) and are intentionally left to the maintainer.
