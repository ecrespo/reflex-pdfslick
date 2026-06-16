"""reflex-pdfslick — a native Reflex component wrapping PDFSlick (PDF.js + Zustand).

Public API (stable surface):

    from reflex_pdfslick import pdf_slick, PdfSlick
    from reflex_pdfslick import ScrollMode, SpreadMode, ScaleValue
    from reflex_pdfslick import PdfSlickOptions
    from reflex_pdfslick import commands

``pdf_slick(url=...)`` renders a reactive PDF viewer; viewer state flows into
Reflex via events (``on_page_change``, ``on_document_load``, ``on_scale_change``,
``on_error``, ``on_metadata``) and Python drives the viewer through the
declarative ``command`` prop built with the ``commands`` helpers.
"""

from . import commands
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
    "commands",
]

__version__ = "0.0.1"
