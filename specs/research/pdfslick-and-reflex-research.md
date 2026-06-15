# Research Notes — PDFSlick & Reflex Component Wrapping

## Metadata

| Field | Value |
|---|---|
| **Author** | Ernesto Crespo |
| **Status** | `REFERENCE` |
| **Version** | 1.0 |
| **Date** | 2026-06-15 |

These notes ground the design in primary sources (PDFSlick repo/docs/npm types,
Reflex docs). They are the evidence base for the PRD, technical, API and
data-model specs.

---

## 1. PDFSlick overview

- Repo: https://github.com/pdfslick/pdfslick · Docs: https://pdfslick.dev
- View & interact with PDFs in React, SolidJS, Svelte and vanilla JS.
- Built on Mozilla **PDF.js**; uses **Zustand** for a reactive store.
- Monorepo packages: `@pdfslick/core` (PDF.js + store), `@pdfslick/react`,
  `@pdfslick/solid`; Svelte uses `@pdfslick/core` directly.
- License: MIT. Author: Vancho Stojkov.

### Versions (June 2026)

- Latest: `@pdfslick/core@4.0.0`, `@pdfslick/react@4.0.0` (released ~Jun 7 2026).
- `@pdfslick/react@4.0.0` deps: `@pdfslick/core@^4.0.0`, `use-sync-external-store`.
- `@pdfslick/core@4.0.0` deps: **`pdfjs-dist@^6.0.227`**, `zustand@^5`.
- React peer: `>=17`. CSS shipped as a single `dist/pdf_viewer.css` (~219 KB).
- **Important:** PDFSlick *package* v4 wraps PDF.js **v6** (not pdf.js v4).

## 2. `@pdfslick/react` API

`usePDFSlick(url, options)` returns:

```ts
{
  isDocumentLoaded: boolean;
  viewerRef: RefCallback<HTMLElement>;
  thumbsRef: RefCallback<HTMLElement>;
  store: StoreApi<PDFSlickState>;
  usePDFSlickStore: <T>(selector?) => T;   // Zustand selector hook
  PDFSlickViewer: Component;
  PDFSlickThumbnails: Component;            // render-prop child
  error: PDFException | null;               // v4 adds error
}
```

- `<PDFSlickViewer>` props: `{ viewerRef, usePDFSlickStore, className? }`.
- `<PDFSlickThumbnails>` is a **render-prop** component: child is
  `(props: {pageNumber,width,height,scale,rotation,loaded,pageLabel,src}) => ReactNode`.
  → **Not expressible from Python** ⇒ thumbnails handled inside the JS wrapper.
- Required CSS: `import "@pdfslick/react/dist/pdf_viewer.css";` (once). Root uses
  the `pdfSlick` class.

### `PDFSlickOptions` (selected)

`scaleValue`, `singlePageViewer`, `removePageBorders`, `enablePrintAutoRotate`,
`useOnlyCssZoom`, `textLayerMode`, `annotationMode`, `annotationEditorMode`,
`thumbnailWidth`, `printResolution`, `maxCanvasPixels`, `filename`,
`getDocumentParams` (pdf.js `DocumentInitParameters`), `onProgress`.

## 3. Imperative API (`pdfSlick` instance)

`loadDocument(url|ArrayBuffer, {filename,onProgress})`, `gotoPage(n)`,
`setRotation(deg)`, `setScrollMode(n)`, `setSpreadMode(n)`,
`increaseScale()/decreaseScale()` (also on `.viewer`), setters
`currentScale = n` / `currentScaleValue = "page-fit"`, `triggerPrinting()`,
`download()/save()/downloadOrSave()`, `openOrDownloadData(bytes, filename)`,
`requestPresentationMode()`, `setAnnotationEditorMode()`,
`setAnnotationEditorParams()`, `getPagesOverview()`, `on/off/dispatch(event)`.

> Gotchas confirmed from example source:
> - **No** `setScale`/`setScaleValue` — use `currentScale`/`currentScaleValue`.
> - Printing is `triggerPrinting()`; download is `downloadOrSave()`.
> - Modes use PDF.js enums re-exported from `@pdfslick/react`:
>   `ScrollMode` (VERTICAL 0, HORIZONTAL 1, WRAPPED 2, PAGE 3),
>   `SpreadMode` (NONE 0, ODD 1, EVEN 2).

## 4. Store schema highlights

Serializable scalars: `isDocumentLoaded, pagesReady, numPages, pageNumber,
scale, scaleValue, pagesRotation, spreadMode, scrollMode, filename, filesize,
title, author, subject, creator, producer, version, isLinearized`.

Non-serializable / careful: `pdfSlick` (class), `thumbnailViews`/`attachments`/
`thumbnails` (JS `Map`), `creationDate`/`modificationDate` (`Date`),
`documentOutline` (contains `Uint8ClampedArray`). See `../data-model/store-schema.md`.

## 5. PDFSlick examples (React, `apps/web/examples`)

| Folder | Demonstrates |
|---|---|
| `SimplePDFViewer/` | basic viewer + bottom nav (`gotoPage`, zoom) |
| `PDFViewerApp/` | full app: Toolbar (ZoomSelector, MoreActionsMenu, SearchBar, DocumentInfo, Freetext/Ink menus), Thumbsbar; exercises most of the API |
| `Comments/` | pin-style comments overlay (external store) — out of scope v1 |
| `MultipleDocuments/` | several independent `usePDFSlick` instances |
| `ThumbnailsLayout/` | thumbnail grid as primary surface |
| `HorizontalThumbs/` | horizontal thumbnail strip |
| `ArrayBuffer/` | load from in-memory bytes |
| `ErrorHandling.tsx` | uses `error` from `usePDFSlick` |

The demo gallery reproduces 7 of these (Comments deferred).

## 6. Reflex wrapping findings

- Current Reflex: **0.9.5.post2** (Jun 2026); 0.9.x component-wrapping API.
- Wrap with `rx.Component` / `rx.NoSSRComponent`: `library`, `tag`,
  `lib_dependencies`, `is_default`, `alias`. Pin versions in `library`/`lib_dependencies`.
- Props are `rx.Var[...]`; snake_case auto-camelCased; `rx.PropsBase` auto-camelCases
  structured props; `_rename_props` handles reserved names (e.g. `style`).
- Events: modern `rx.EventHandler[spec]` with lambda specs (`lambda e0: [e0]`),
  or helpers like `rx.event.passthrough_event_spec(int)`.
- **NoSSR:** `rx.NoSSRComponent` emits `next/dynamic(..., {ssr:false})`. Required
  for PDF.js (browser-only).
- CSS/assets: `add_imports({"": "pkg/dist/file.css"})`; `add_custom_code`,
  `add_hooks`, `add_style`; static via `assets/` and `rx.asset(..., shared=True)`.
- **Hook-based libs:** Reflex recommends writing a small **local `.tsx`**
  wrapper that calls the hook and exposes plain props/events, then wrapping that
  via `library = f"$/public{rx.asset('./wrapper.tsx', shared=True)}"` with the
  npm package in `lib_dependencies`. This is exactly PDFSlick's situation.
- Custom-component project: `reflex component init` → `custom_components/`,
  demo app, `pyproject.toml`; build with `reflex component build`; publish via
  `twine`/`uv` (Reflex does not publish for you).

## 7. Key references

- PDFSlick: https://pdfslick.dev/docs , https://pdfslick.dev/examples ,
  npm `@pdfslick/core`, `@pdfslick/react` v4 type definitions.
- Reflex: reflex.dev/docs/wrapping-react/* , reflex.dev/docs/custom-components/* ,
  reflex.dev/docs/assets/overview.
