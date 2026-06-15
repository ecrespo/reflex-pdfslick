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
 * STATUS: Phase-1 reference implementation (see specs/plans/implementation-plan.md).
 * It is committed as the base artifact for the runtime; build integration and
 * imperative-control dispatch are finalized in Phases 1–3.
 */
import * as React from "react";
import {
  usePDFSlick,
  PDFSlickViewer,
  PDFSlickThumbnails,
} from "@pdfslick/react";
import "@pdfslick/react/dist/pdf_viewer.css";

export type PdfSlickWrapperProps = {
  url: string;
  scaleValue?: string;
  singlePageViewer?: boolean;
  removePageBorders?: boolean;
  thumbnailWidth?: number;
  showThumbnails?: boolean;
  onDocumentLoad?: (numPages: number) => void;
  onPageChange?: (page: number) => void;
  onScaleChange?: (scale: number) => void;
  onError?: (err: unknown) => void;
};

export function PdfSlickWrapper({
  url,
  scaleValue = "page-fit",
  singlePageViewer = false,
  removePageBorders = false,
  thumbnailWidth = 212,
  showThumbnails = false,
  onDocumentLoad,
  onPageChange,
  onScaleChange,
  onError,
}: PdfSlickWrapperProps) {
  const {
    viewerRef,
    thumbsRef,
    usePDFSlickStore,
    PDFSlickViewer: Viewer,
    error,
  } = usePDFSlick(url, {
    scaleValue,
    singlePageViewer,
    removePageBorders,
    thumbnailWidth,
  });

  const pageNumber = usePDFSlickStore((s) => s.pageNumber);
  const numPages = usePDFSlickStore((s) => s.numPages);
  const scale = usePDFSlickStore((s) => s.scale);
  const isLoaded = usePDFSlickStore((s) => s.isDocumentLoaded);

  React.useEffect(() => {
    if (isLoaded) onDocumentLoad?.(numPages);
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
    if (error) onError?.(error);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [error]);

  if (error) {
    return (
      <div className="pdfSlick" style={{ padding: "1rem", color: "#b91c1c" }}>
        Failed to load PDF.
      </div>
    );
  }

  return (
    <div className="pdfSlick" style={{ position: "absolute", inset: 0, display: "flex" }}>
      {showThumbnails && (
        <div style={{ width: 240, overflow: "auto" }}>
          <PDFSlickThumbnails {...{ thumbsRef, usePDFSlickStore }}>
            {({ pageNumber: pn, src, pageLabel, loaded }) => (
              <div style={{ padding: 8 }}>
                {loaded && src ? (
                  <img src={src} alt={`Page ${pageLabel ?? pn}`} />
                ) : (
                  <div style={{ height: 280, background: "#e5e7eb" }} />
                )}
              </div>
            )}
          </PDFSlickThumbnails>
        </div>
      )}
      <div style={{ flex: 1, position: "relative" }}>
        <Viewer {...{ viewerRef, usePDFSlickStore }} />
      </div>
    </div>
  );
}

export default PdfSlickWrapper;
