/**
 * PdfSlickWrapper — local React wrapper around `@pdfslick/react`.
 *
 * PDFSlick's public surface is the hook `usePDFSlick(url, options)`, not a
 * drop-in component, and `<PDFSlickThumbnails>` uses a render-prop child that
 * cannot be expressed from Python. This thin wrapper calls the hook internally,
 * renders `<PDFSlickViewer>` (and optional thumbnails), subscribes to the
 * Zustand store via `usePDFSlickStore`, and exposes a clean prop/event API for
 * the Reflex `PdfSlick` component to bind to.
 *
 * It is browser-only (PDF.js), so the Reflex side wraps it as a NoSSRComponent.
 *
 * Responsibilities by phase:
 *  - Phase 1: call the hook, render the viewer, import CSS.
 *  - Phase 2: subscribe to store slices, forward serializable scalars to Reflex
 *    events (page, scale, load, error, metadata). Only serializable values
 *    cross the boundary; Dates become ISO strings, Maps become arrays.
 *  - Phase 3: apply declarative `command` objects (goto/zoom/rotate/modes/
 *    print/download) against the imperative `pdfSlick` instance, apply-once.
 *  - Phase 4: render an optional thumbnails sidebar (vertical or horizontal).
 */
import * as React from "react";
import { GlobalWorkerOptions } from "pdfjs-dist";
// Vite resolves `?url` to a served/hashed asset URL for the worker file. This
// uses the SAME hoisted `pdfjs-dist` instance that `@pdfslick/core` imports, so
// the worker version always matches the PDF.js API version.
import pdfWorkerUrl from "pdfjs-dist/build/pdf.worker.min.mjs?url";
import { usePDFSlick, PDFSlickViewer, PDFSlickThumbnails } from "@pdfslick/react";
import "@pdfslick/react/dist/pdf_viewer.css";

// PDF.js worker fix. `@pdfslick/core` sets
//   GlobalWorkerOptions.workerSrc = new URL('pdfjs-dist/build/pdf.worker.min.mjs', import.meta.url)
// at module load, which resolves RELATIVE to the core module directory
// (.../@pdfslick/core/dist/esm/pdfjs-dist/build/...) — a path that does not
// exist under Reflex's Vite server, so the worker fails to load ("Setting up
// fake worker failed"). All ES imports above are evaluated before this module
// body runs, so core's (broken) assignment has already happened; we override it
// here with the correctly-resolved worker URL on the same GlobalWorkerOptions.
if (pdfWorkerUrl) {
  GlobalWorkerOptions.workerSrc = pdfWorkerUrl as string;
}

type PdfCommand = {
  action?: string;
  page?: number;
  value?: number | string;
  mode?: number;
  degrees?: number;
};

export type PdfSlickWrapperProps = {
  url: string;
  scaleValue?: string;
  singlePageViewer?: boolean;
  removePageBorders?: boolean;
  thumbnailWidth?: number;
  showThumbnails?: boolean;
  horizontalThumbnails?: boolean;
  command?: PdfCommand | null;
  onDocumentLoad?: (numPages: number) => void;
  onPageChange?: (page: number) => void;
  onScaleChange?: (scale: number) => void;
  onError?: (err: { name: string; message: string }) => void;
  onMetadata?: (meta: Record<string, unknown>) => void;
};

/** Convert a possible Date to an ISO string; pass through null/undefined. */
function toIso(value: unknown): string | null {
  if (value instanceof Date && !isNaN(value.getTime())) return value.toISOString();
  if (typeof value === "string" && value) return value;
  return null;
}

/** Normalize an unknown error into a serializable {name, message} object. */
function normalizeError(error: unknown): { name: string; message: string } {
  if (error && typeof error === "object") {
    const e = error as { name?: string; message?: string };
    return { name: e.name ?? "Error", message: e.message ?? String(error) };
  }
  return { name: "Error", message: String(error) };
}

export function PdfSlickWrapper({
  url,
  scaleValue = "page-fit",
  singlePageViewer = false,
  removePageBorders = false,
  thumbnailWidth = 212,
  showThumbnails = false,
  horizontalThumbnails = false,
  command = null,
  onDocumentLoad,
  onPageChange,
  onScaleChange,
  onError,
  onMetadata,
}: PdfSlickWrapperProps) {
  const { viewerRef, thumbsRef, usePDFSlickStore, error } = usePDFSlick(url, {
    scaleValue,
    singlePageViewer,
    removePageBorders,
    thumbnailWidth,
  });

  const pageNumber = usePDFSlickStore((s) => s.pageNumber);
  const numPages = usePDFSlickStore((s) => s.numPages);
  const scale = usePDFSlickStore((s) => s.scale);
  const isLoaded = usePDFSlickStore((s) => s.isDocumentLoaded);
  const pdfSlick = usePDFSlickStore((s) => s.pdfSlick);
  const store = usePDFSlickStore((s) => s);

  // --- Phase 2: forward store changes to Reflex events --------------------
  React.useEffect(() => {
    if (!isLoaded) return;
    onDocumentLoad?.(numPages);
    if (onMetadata) {
      onMetadata({
        numPages,
        title: store.title ?? "",
        author: store.author ?? "",
        subject: store.subject ?? "",
        creator: store.creator ?? "",
        producer: store.producer ?? "",
        version: store.version ?? "",
        filename: store.filename ?? "",
        filesize: store.filesize ?? 0,
        isLinearized: !!store.isLinearized,
        creationDate: toIso(store.creationDate),
        modificationDate: toIso(store.modificationDate),
      });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isLoaded, numPages]);

  React.useEffect(() => {
    onPageChange?.(pageNumber);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pageNumber]);

  React.useEffect(() => {
    onScaleChange?.(scale);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [scale]);

  React.useEffect(() => {
    if (error) onError?.(normalizeError(error));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [error]);

  // --- Phase 3: apply declarative commands once ---------------------------
  const lastCommandKey = React.useRef<string>("");
  React.useEffect(() => {
    if (!command || !command.action || !pdfSlick) return;
    const key = JSON.stringify(command);
    if (key === lastCommandKey.current) return;
    lastCommandKey.current = key;

    const ps = pdfSlick as any;
    const current = store.pageNumber ?? 1;
    const total = store.numPages ?? 1;
    switch (command.action) {
      case "goto":
        if (typeof command.page === "number") ps.gotoPage(command.page);
        break;
      case "next":
        ps.gotoPage(Math.min(total, current + 1));
        break;
      case "prev":
        ps.gotoPage(Math.max(1, current - 1));
        break;
      case "zoomIn":
        (ps.viewer ?? ps).increaseScale?.();
        break;
      case "zoomOut":
        (ps.viewer ?? ps).decreaseScale?.();
        break;
      case "zoomPreset":
        if (command.value != null) ps.currentScaleValue = String(command.value);
        break;
      case "zoomValue":
        if (command.value != null) ps.currentScale = Number(command.value);
        break;
      case "rotate":
        if (typeof command.degrees === "number") {
          const base = store.pagesRotation ?? 0;
          ps.setRotation(base + command.degrees);
        }
        break;
      case "scrollMode":
        if (typeof command.mode === "number") ps.setScrollMode(command.mode);
        break;
      case "spreadMode":
        if (typeof command.mode === "number") ps.setSpreadMode(command.mode);
        break;
      case "print":
        ps.triggerPrinting?.();
        break;
      case "download":
        ps.downloadOrSave?.();
        break;
      default:
        break;
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [command, pdfSlick]);

  if (error) {
    return (
      <div className="pdfSlick" style={{ padding: "1rem", color: "#b91c1c" }}>
        Failed to load PDF: {normalizeError(error).message}
      </div>
    );
  }

  const horizontal = showThumbnails && horizontalThumbnails;
  const thumbsPanel = showThumbnails ? (
    <div
      ref={thumbsRef as any}
      className="pdfSlickThumbs"
      style={
        horizontal
          ? { height: 160, width: "100%", overflowX: "auto", display: "flex", gap: 8, padding: 8 }
          : { width: 240, height: "100%", overflowY: "auto", padding: 8 }
      }
    >
      <PDFSlickThumbnails {...{ thumbsRef, usePDFSlickStore }}>
        {({ pageNumber: pn, src, pageLabel, loaded }) => (
          <div
            key={pn}
            onClick={() => pdfSlick?.gotoPage(pn)}
            style={{
              cursor: "pointer",
              padding: 4,
              outline: pn === pageNumber ? "2px solid #2563eb" : "1px solid #e5e7eb",
              borderRadius: 4,
            }}
          >
            {loaded && src ? (
              <img src={src} alt={`Page ${pageLabel ?? pn}`} style={{ display: "block", width: "100%" }} />
            ) : (
              <div style={{ height: horizontal ? 120 : 260, width: 160, background: "#e5e7eb" }} />
            )}
          </div>
        )}
      </PDFSlickThumbnails>
    </div>
  ) : null;

  return (
    <div
      className="pdfSlick"
      style={{
        position: "absolute",
        inset: 0,
        display: "flex",
        flexDirection: horizontal ? "column" : "row",
      }}
    >
      {showThumbnails && !horizontal && thumbsPanel}
      {showThumbnails && horizontal && thumbsPanel}
      <div style={{ flex: 1, position: "relative" }}>
        <PDFSlickViewer {...{ viewerRef, usePDFSlickStore }} />
      </div>
    </div>
  );
}

export default PdfSlickWrapper;
