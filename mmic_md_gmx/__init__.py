"""
mmic_md_gmx
MD simulation via GMX engine
"""

# Add imports here
from .mmic_mmic_md_gmx import *
from . import models, components

# Handle versioneer
from ._version import get_versions

versions = get_versions()
__version__ = versions["version"]
__git_revision__ = versions["full-revisionid"]
del get_versions, versions


