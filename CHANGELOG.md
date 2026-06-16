# Changelog

All notable changes to `reflex-pdfslick` are documented here. The format is
based on [Keep a Changelog](https://keepachangelog.com/) and this project
adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added — Phase 0 (Foundation & SDD)
- Repository scaffold: `custom_components/`, `specs/`, `tests/`, `pdfslick_demo/`.
- Packaging: `pyproject.toml`, `LICENSE` (MIT), `.gitignore`, `README.md`.
- Full Spec-Driven Design documentation set under `specs/`:
  PRD, technical architecture, API spec, data model, implementation plan,
  task breakdown, and research notes.
- Python package scaffold: `PdfSlick` component contract, `PdfSlickOptions`,
  and `ScrollMode` / `SpreadMode` / `ScaleValue` enums.
- Reference React wrapper `PdfSlickWrapper.tsx`.
- Demo app skeleton with the planned example gallery index.
- Unit tests for enums, options, and the import surface.

### Added — Phases 1–6 (Component runtime, demo gallery, CI)
- **Core wrapper (Phase 1):** `PdfSlick(rx.NoSSRComponent)` wired to the local
  `PdfSlickWrapper.tsx` via `rx.asset(..., shared=True).importable_path`
  (`$/public` module path), `tag="PdfSlickWrapper"`, `lib_dependencies`
  pinned to `@pdfslick/react@4.0.0`, and `pdf_viewer.css` imported once via
  `add_imports`. Props: `url`, `scale_value`, `single_page_viewer`,
  `remove_page_borders`, `thumbnail_width`, `show_thumbnails`,
  `horizontal_thumbnails`.
- **Events & state bridge (Phase 2):** `on_document_load`, `on_page_change`,
  `on_scale_change`, `on_error`, `on_metadata`. The wrapper subscribes to the
  Zustand store and forwards only serializable scalars; errors are normalized to
  `{name, message}` and dates to ISO strings.
- **Imperative controls (Phase 3):** declarative `command` prop applied
  apply-once by the wrapper, with `reflex_pdfslick.commands` helpers
  (`goto_page`, `next_page`/`prev_page`, `zoom_in`/`zoom_out`,
  `set_zoom_preset`/`set_zoom_value`, `rotate`, `set_scroll_mode`/
  `set_spread_mode`, `print_document`, `download`).
- **Thumbnails & multi-document (Phase 4):** vertical and horizontal thumbnail
  layouts (click-to-goto); multiple independent viewers per page.
- **Demo gallery (Phase 5):** all 7 PDFSlick examples reproduced as routes
  (`simple`, `full`, `thumbnails`, `horizontal`, `multiple`, `arraybuffer`,
  `error`), each a unit-tested pure builder in `examples.py`.
- **Tests & CI (Phase 6):** 35 Python unit tests (enums, options, component
  wiring, events, command serialization, thumbnails, demo builders); GitHub
  Actions running pytest across Python 3.10–3.13, an esbuild TSX-transpile
  check, and a Reflex demo frontend-build smoke job.

### Fixed
- `rx.asset` shared-asset symlinking fails for nested paths (`js/...`); the
  wrapper now lives beside `pdfslick.py` and is referenced by bare filename so
  the `$/public` library path resolves in the Reflex build.
- **PDF.js worker failed to load** ("Setting up fake worker failed"):
  `@pdfslick/core` sets `GlobalWorkerOptions.workerSrc` via
  `new URL('pdfjs-dist/build/pdf.worker.min.mjs', import.meta.url)`, which under
  Reflex's Vite build resolves relative to the core module directory to a
  non-existent path. The wrapper now overrides `workerSrc` with a Vite-resolved
  asset URL (`pdfjs-dist/build/pdf.worker.min.mjs?url`) on the same hoisted
  `pdfjs-dist` instance, and `pdfjs-dist@^6.0.227` is declared in
  `lib_dependencies` to guarantee a single shared copy (worker matches API).

### Packaging — Reflex custom component
- `pyproject.toml` carries the `reflex-custom-components` keyword (Reflex gallery
  discovery) and `twine` in the dev extra; wheel/sdist include the
  `PdfSlickWrapper.tsx` wrapper and the generated `pdfslick.pyi` type stub.
- `reflex component build` produces installable artifacts; documented build/
  publish/share workflow in the README.

### Verified
- The demo compiles to a Reflex production build (`reflex export
  --frontend-only`): `@pdfslick/react@4.0.0` resolves, the local wrapper is
  bundled, and the Next.js production build succeeds.

[Unreleased]: https://github.com/ecrespo/reflex-pdfslick/commits/main
