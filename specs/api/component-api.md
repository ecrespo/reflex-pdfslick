# reflex-pdfslick — Public API Specification

## Metadata

| Field | Value |
|---|---|
| **Author** | Ernesto Crespo |
| **Status** | `APPROVED` |
| **Version** | 1.0 |
| **Date** | 2026-06-15 |
| **Related PRD** | `../prd/pdfslick-component.md` |
| **Related Tech Design** | `../technical/architecture.md` |
| **Related Data Model** | `../data-model/store-schema.md` |

---

## 1. Import surface

```python
from reflex_pdfslick import (
    pdf_slick,        # factory: PdfSlick.create
    PdfSlick,         # component class
    PdfSlickOptions,  # typed options (rx.PropsBase)
    ScaleValue,       # str enum: AUTO, PAGE_ACTUAL, PAGE_FIT, PAGE_WIDTH
    ScrollMode,       # int enum: VERTICAL, HORIZONTAL, WRAPPED, PAGE
    SpreadMode,       # int enum: NONE, ODD, EVEN
)
```

## 2. `pdf_slick(...)` props

Snake_case in Python; emitted as camelCase to JS.

| Prop | Type | Default | JS name | Description |
|---|---|---|---|---|
| `url` | `str \| rx.Var[str]` | — (required) | `url` | Path/URL of the PDF document. |
| `scale_value` | `str` | `"page-fit"` | `scaleValue` | `"auto" \| "page-actual" \| "page-fit" \| "page-width"` or a numeric string (e.g. `"1.5"`). |
| `single_page_viewer` | `bool` | `False` | `singlePageViewer` | Show a single page at a time. |
| `remove_page_borders` | `bool` | `False` | `removePageBorders` | Hide page borders. |
| `thumbnail_width` | `int` | `212` | `thumbnailWidth` | Width (px) of generated thumbnails. |
| `show_thumbnails` | `bool` | `False` | `showThumbnails` | Render the thumbnails sidebar. |

Standard Reflex style props (`width`, `height`, `class_name`, `style`, ...) are
accepted and applied to the component's root container. A definite height (e.g.
`height="700px"`) is recommended since the viewer fills its container.

### 2.1 `PdfSlickOptions`

For advanced configuration, pass a `PdfSlickOptions` instance via the `options`
prop (Phase 1+). Fields mirror PDFSlick's `PDFSlickOptions`:

| Field | Type | JS name |
|---|---|---|
| `scale_value` | `str` | `scaleValue` |
| `single_page_viewer` | `bool` | `singlePageViewer` |
| `remove_page_borders` | `bool` | `removePageBorders` |
| `enable_print_auto_rotate` | `bool` | `enablePrintAutoRotate` |
| `use_only_css_zoom` | `bool` | `useOnlyCssZoom` |
| `text_layer_mode` | `int` | `textLayerMode` |
| `annotation_mode` | `int` | `annotationMode` |
| `annotation_editor_mode` | `int` | `annotationEditorMode` |
| `thumbnail_width` | `int` | `thumbnailWidth` |
| `print_resolution` | `int` | `printResolution` |
| `max_canvas_pixels` | `int` | `maxCanvasPixels` |
| `filename` | `str` | `filename` |
| `extra` | `dict` | merged verbatim (e.g. `getDocumentParams`) |

## 3. Events

| Event | Python handler signature | Payload | Fired when |
|---|---|---|---|
| `on_document_load` | `(self, num_pages: int)` | total page count | document finishes loading |
| `on_page_change` | `(self, page: int)` | current 1-based page | current page changes |
| `on_scale_change` | `(self, scale: float)` | current numeric scale | zoom level changes |
| `on_error` | `(self, err: dict)` | `{name, message}` | load/parse fails |

Example:

```python
class State(rx.State):
    page: int = 1
    total: int = 0

    @rx.event
    def set_page(self, page: int):
        self.page = page

    @rx.event
    def set_total(self, total: int):
        self.total = total


def view() -> rx.Component:
    return pdf_slick(
        url="/sample.pdf",
        scale_value=ScaleValue.PAGE_WIDTH,
        on_page_change=State.set_page,
        on_document_load=State.set_total,
        height="700px",
    )
```

## 4. Imperative controls (Phase 3)

Driven declaratively through a `command` prop the wrapper applies then clears.
The proposed Python helper surface:

| Helper | Effect | Underlying PDFSlick call |
|---|---|---|
| go to page `n` | jump to page | `pdfSlick.gotoPage(n)` |
| next / previous page | relative nav | `gotoPage(page ± 1)` |
| zoom in / out | step zoom | `viewer.increaseScale()` / `decreaseScale()` |
| set zoom preset | `"page-fit"`, ... | `pdfSlick.currentScaleValue = preset` |
| set zoom value `x` | absolute scale | `pdfSlick.currentScale = x` |
| rotate `±90` | rotate pages | `pdfSlick.setRotation(deg)` |
| set scroll mode | vertical/horizontal/wrapped/page | `pdfSlick.setScrollMode(ScrollMode.*)` |
| set spread mode | none/odd/even | `pdfSlick.setSpreadMode(SpreadMode.*)` |
| print | open print dialog | `pdfSlick.triggerPrinting()` |
| download / save | save file | `pdfSlick.downloadOrSave()` |

> **Note (from research):** PDFSlick has **no** `setScale`/`setScaleValue`
> methods — zoom uses the `currentScale` / `currentScaleValue` setters. Printing
> is `triggerPrinting()` (not `requestPrint`). These are reflected above.

## 5. Enums

```python
class ScrollMode(IntEnum):   # PDF.js values
    VERTICAL = 0
    HORIZONTAL = 1
    WRAPPED = 2
    PAGE = 3

class SpreadMode(IntEnum):
    NONE = 0
    ODD = 1
    EVEN = 2

class ScaleValue(str, Enum):
    AUTO = "auto"
    PAGE_ACTUAL = "page-actual"
    PAGE_FIT = "page-fit"
    PAGE_WIDTH = "page-width"
```

## 6. Versioning & stability

- Public symbols listed in §1 are the stable surface.
- The npm dependency is pinned to `@pdfslick/react@4.0.0`.
- Breaking changes follow semver and are recorded in GitHub Releases.
