# reflex-pdfslick — Data Model & Store Schema

## Metadata

| Field | Value |
|---|---|
| **Author** | Ernesto Crespo |
| **Status** | `APPROVED` |
| **Version** | 1.0 |
| **Date** | 2026-06-15 |
| **Related Tech Design** | `../technical/architecture.md` |
| **Related API Spec** | `../api/component-api.md` |

---

## 1. PDFSlick store (`PDFSlickState`)

`@pdfslick/core` exposes a Zustand store. The fields below are taken from the
v4 type definitions (`PDFSlickStateProps`). Each row notes whether it is safely
serializable across the JS → Python boundary.

| Field | Type (JS) | Serializable | Notes |
|---|---|---|---|
| `isDocumentLoaded` | `boolean` | ✅ | document ready flag |
| `pagesReady` | `boolean` | ✅ | pages rendered flag |
| `numPages` | `number` | ✅ | total pages |
| `pageNumber` | `number` | ✅ | current 1-based page |
| `scale` | `number` | ✅ | numeric zoom |
| `scaleValue` | `string \| undefined` | ✅ | preset or numeric string |
| `pagesRotation` | `number` | ✅ | degrees |
| `spreadMode` | `number` | ✅ | `SpreadMode` |
| `scrollMode` | `number` | ✅ | `ScrollMode` |
| `url` | `string \| ArrayBuffer \| null` | ⚠️ | string only |
| `filename` | `string` | ✅ | |
| `filesize` | `number` | ✅ | bytes |
| `title` / `author` / `subject` / `creator` / `producer` / `version` | `string` | ✅ | metadata |
| `keywords` | `any` | ⚠️ | normalize to string/list |
| `creationDate` / `modificationDate` | `Date \| null` | ⚠️ | convert to ISO string |
| `pageSize` | `any` | ⚠️ | `{width,height}` if needed |
| `isLinearized` | `boolean` | ✅ | |
| `documentOutline` | `TPDFDocumentOutline \| null` | ⚠️ | tree; contains `Uint8ClampedArray` color → drop/convert |
| `attachments` | `Map<string, {...}>` | ❌ | JS Map; out of scope v1 |
| `annotationEditorMode` | `number` | ✅ | |
| `thumbnailViews` | `Map<number, PDFThumbnailView>` | ❌ | DOM view objects |
| `thumbnails` | `Map<number, {pageNumber,width,height,scale,rotation,loaded,pageLabel,src}>` | ⚠️ | values serializable; container is a Map → convert to array |
| `pdfSlick` | `PDFSlick \| null` | ❌ | imperative instance (kept in JS only) |

## 2. Boundary rules

1. **Only serializable scalars cross to Python.** The wrapper never emits
   `Map`, `Date`, `Uint8ClampedArray`, or the `pdfSlick` instance.
2. **Dates → ISO strings.** `creationDate`/`modificationDate` are converted with
   `.toISOString()` before emission.
3. **Maps → arrays/objects.** `thumbnails` is converted to a sorted array of
   plain objects when (and if) exposed.
4. **The `pdfSlick` instance stays in JS.** Imperative actions are invoked
   inside the wrapper in response to the declarative `command` prop.

## 3. Python-side state model (recommended app pattern)

The component does not own application state; the demo and downstream apps keep
the slices they care about. Recommended shape:

```python
class PdfState(rx.State):
    # synced via events
    page_number: int = 1
    num_pages: int = 0
    scale: float = 1.0
    is_loaded: bool = False
    error: dict = {}

    # metadata (Phase 2+, optional on_metadata event)
    title: str = ""
    author: str = ""

    @rx.event
    def on_page_change(self, page: int):
        self.page_number = page

    @rx.event
    def on_document_load(self, num_pages: int):
        self.num_pages = num_pages
        self.is_loaded = True

    @rx.event
    def on_scale_change(self, scale: float):
        self.scale = scale

    @rx.event
    def on_error(self, err: dict):
        self.error = err
```

## 4. Options serialization

`PdfSlickOptions` (an `rx.PropsBase`) serializes snake_case → camelCase:

| Python | JS |
|---|---|
| `single_page_viewer=True` | `singlePageViewer: true` |
| `scale_value="page-fit"` | `scaleValue: "page-fit"` |
| `thumbnail_width=212` | `thumbnailWidth: 212` |
| `extra={"getDocumentParams": {...}}` | merged verbatim |

## 5. Enum value mapping

| Enum | Python | JS numeric (PDF.js) |
|---|---|---|
| ScrollMode | `VERTICAL/HORIZONTAL/WRAPPED/PAGE` | `0/1/2/3` |
| SpreadMode | `NONE/ODD/EVEN` | `0/1/2` |
| ScaleValue | `AUTO/PAGE_ACTUAL/PAGE_FIT/PAGE_WIDTH` | `"auto"/"page-actual"/"page-fit"/"page-width"` |
