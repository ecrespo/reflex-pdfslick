# Changelog

All notable changes to `reflex-pdfslick` are documented here. The format is
based on [Keep a Changelog](https://keepachangelog.com/) and this project
adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] - 2026-10-24

### Changed
- **Reflex 0.10:** the package now requires `reflex>=0.10.0` (was `>=0.9.0`).
  The component-wrapping API is unchanged; the wrapper, events and commands work
  as-is on Reflex 0.10 (React 19, React Router 8, Vite 8 frontend).
- **Python >= 3.11:** dropped Python 3.10 to match Reflex 0.10's own
  `requires-python`. Added explicit 3.11/3.12/3.13 trove classifiers.
- Build backend requirement raised to `setuptools>=78.1.1`.
- Packaging docs: the `reflex component build/share` CLI was removed in
  Reflex 0.10; the README now documents `uv build` + `twine check` and stub
  regeneration via `python -m reflex_base.utils.pyi_generator`. The committed
  `pdfslick.pyi` was regenerated with Reflex 0.10 (no changes).
- Added the `reflex-component` PyPI keyword (used by Reflex's component
  template) alongside `reflex-custom-components`.
- Demo `requirements.txt` now requires `reflex>=0.10.0`.
- Docs: README gains a *Requirements* table and an *Automated release* section;
  specs updated from Next.js / `next/dynamic` to Reflex's current React Router +
  Vite output (`ClientSide(() => import(...))` for `NoSSRComponent`).

### CI
- All workflows run on **Node 24** (`actions/setup-node` `node-version: "24"`)
  and use the current major versions of `actions/checkout`, `actions/setup-node`
  and `astral-sh/setup-uv`.
- Test matrix: Python 3.11–3.13.
- New `publish.yml` workflow: on a `vX.Y.Z` tag pointing at `main`, verifies the
  tag matches the package version, runs the tests, builds sdist + wheel,
  publishes to PyPI and creates the GitHub Release.

## [0.0.1] - 2026-06-15

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
  Actions running pytest across Python 3.10–3.13 (3.11–3.13 since 0.1.0), an esbuild TSX-transpile
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

[Unreleased]: https://github.com/ecrespo/reflex-pdfslick/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/ecrespo/reflex-pdfslick/compare/v0.0.1...v0.1.0
[0.0.1]: https://github.com/ecrespo/reflex-pdfslick/releases/tag/v0.0.1
