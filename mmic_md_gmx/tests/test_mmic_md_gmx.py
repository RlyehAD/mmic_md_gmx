"""
Unit and regression test for the mmic_md_gmx package.
"""

# Import package, test suite, and other packages as needed
import mmelemental
import mmic_md
from mmic_md import InputMD, OutputMD
from mmelemental.models import Molecule, Trajectory, ForceField
import mmic_md_gmx

from mmic_md_gmx.components import MDGmxComponent

import mm_data
import mmic_md_gmx
import pytest
import sys


def test_mmic_md_gmx_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "mmic_md_gmx" in sys.modules


def test_md_component():
    """
    This test reads data from mmic_data and tries to run a short MD simulation.
    """

    mol = mmelemental.models.Molecule.from_file(mm_data.mols["water-mol.json"])
    ff = mmelemental.models.ForceField.from_file(mm_data.ffs["water-ff.json"])

    inputs = mmic_md.InputMD(
        engine="gmx",
        schema_name="test",
        schema_version=1.0,
        system = {mol:ff},
        boundary=(
            "periodic",
            "periodic",
            "periodic",
            "periodic",
            "periodic",
            "periodic",
        ),
        max_steps=20,
        step_size=0.01,
        method="md",
        freq_write={"nstxout": 5, "nstvout": 5, "nstenergy": 5, "nstlog": 5},
        long_forces={"method": "PME"},
        short_forces={"method": "Cutoff"},
        temp_couple={
            "tcoupl": "Berendsen",
            "tc-grps": "system",
            "tau-t": 0.1,
            "ref-t": 300,
        },
        press_couple={"pcoupl": "no"},
    )

    outputs = MDGmxComponent.compute(inputs)
