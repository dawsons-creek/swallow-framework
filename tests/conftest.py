"""
Configuration for pytest.
"""

import sys
import os
import pytest

# Make sure the package is importable during tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
