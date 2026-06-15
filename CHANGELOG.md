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
- Reference React wrapper `js/PdfSlickWrapper.tsx`.
- Demo app skeleton with the planned example gallery index.
- Unit tests for enums, options, and the import surface.

### Planned
- Phases 1–6 per `specs/plans/implementation-plan.md`: core wrapper, events,
  imperative controls, thumbnails, demo gallery, tests/CI/PyPI release.

[Unreleased]: https://github.com/ecrespo/reflex-pdfslick/commits/main
