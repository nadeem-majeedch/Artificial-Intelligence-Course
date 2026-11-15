"""Shared test configuration.

Every module keeps its reference code in ``modules/<module>/code``. The tests import
those modules by their file names (``import search_algorithms as sa``), so this file
puts every code directory on ``sys.path`` once, in a deterministic order.
"""

import glob
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

for directory in sorted(glob.glob(os.path.join(ROOT, "modules", "*", "code"))):
    if directory not in sys.path:
        sys.path.insert(0, directory)

for directory in sorted(glob.glob(os.path.join(ROOT, "prerequisites", "*", "code"))):
    if directory not in sys.path:
        sys.path.insert(0, directory)
