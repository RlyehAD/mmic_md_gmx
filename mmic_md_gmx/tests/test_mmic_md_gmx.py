"""
Unit and regression test for the mmic_md_gmx package.
"""

# Import package, test suite, and other packages as needed
import mmic_md_gmx
import pytest
import sys


def test_mmic_md_gmx_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "mmic_md_gmx" in sys.modules
