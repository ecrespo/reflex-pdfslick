"""Enums and value types mirroring PDFSlick / PDF.js constants.

These mirror the numeric enums re-exported by ``@pdfslick/react`` (originally
from PDF.js ``ui_utils``) and the accepted ``scaleValue`` strings. Keeping them
in Python lets the demo app and downstream users avoid magic numbers.

References:
- ``specs/data-model/store-schema.md``
- ``specs/api/component-api.md``
"""

from __future__ import annotations

from enum import Enum, IntEnum


class ScrollMode(IntEnum):
    """PDF.js scroll modes (values match ``pdfjs-dist`` ``ScrollMode``)."""

    VERTICAL = 0
    HORIZONTAL = 1
    WRAPPED = 2
    PAGE = 3


class SpreadMode(IntEnum):
    """PDF.js spread modes (values match ``pdfjs-dist`` ``SpreadMode``)."""

    NONE = 0
    ODD = 1
    EVEN = 2


class ScaleValue(str, Enum):
    """Named zoom presets accepted by PDFSlick's ``scaleValue`` option.

    A numeric string (e.g. ``"1.5"``) is also valid and maps to an absolute
    scale; use it directly as a plain ``str`` where a preset is not enough.
    """

    AUTO = "auto"
    PAGE_ACTUAL = "page-actual"
    PAGE_FIT = "page-fit"
    PAGE_WIDTH = "page-width"

    def __str__(self) -> str:  # pragma: no cover - convenience
        return self.value
