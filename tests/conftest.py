"""Pytest configuration for the Python-only unit suite.

``reflex_pdfslick.pdfslick`` calls ``rx.asset(..., shared=True)`` at import time
to resolve the local JS wrapper into a ``$/public`` library path. In a full
``reflex`` compile that also symlinks the asset into the app's ``assets/``
directory. For the headless unit tests we only need the resolved path, not the
symlink, so we run Reflex in backend-only mode to avoid creating stray
``assets/external`` directories in the repo during ``pytest``.

This must be set before ``reflex`` reads the asset, which happens when a test
module first imports ``reflex_pdfslick``; ``conftest`` is imported by pytest
before any test module, so setting it here is early enough.
"""

import os

os.environ.setdefault("REFLEX_BACKEND_ONLY", "1")