"""reflex-pdfslick — a native Reflex component wrapping PDFSlick (PDF.js + Zustand).

Public API (stable surface):

    from reflex_pdfslick import pdf_slick, PdfSlick
    from reflex_pdfslick import ScrollMode, SpreadMode, ScaleValue
    from reflex_pdfslick import PdfSlickOptions

The component runtime is delivered incrementally per
``specs/plans/implementation-plan.md``. Until Phase 1 lands, ``pdf_slick`` is a
documented scaffold that raises ``NotImplementedError`` when created, so the
package imports cleanly and the API contract is discoverable.
"""

from .models import ScaleValue, ScrollMode, SpreadMode
from .options import PdfSlickOptions
from .pdfslick import PdfSlick, pdf_slick

__all__ = [
    "PdfSlick",
    "pdf_slick",
    "PdfSlickOptions",
    "ScaleValue",
    "ScrollMode",
    "SpreadMode",
]

__version__ = "0.0.1"
