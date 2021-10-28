# Molecular Dynamics Component

[//]: # (Badges)
[![GitHub Actions Build Status](https://github.com/RlyehAD/mmic_md_gmx/workflows/CI/badge.svg)](https://github.com/RlyehAD/mmic_md_gmx/actions?query=workflow%3ACI)
[![codecov](https://codecov.io/gh/RlyehAD/mmic_md_gmx/branch/master/graph/badge.svg)](https://codecov.io/gh/RlyehAD/mmic_md_gmx/branch/master)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/RlyehAD/mmic_md_gmx.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/RlyehAD/mmic_md_gmx/context:python)


This is part of the [MolSSI](http://molssi.org) Molecular Mechanics Interoperable Components ([MMIC](https://github.com/MolSSI/mmic)) project. This package provides a Tactic component for [mmic_md](https://github.com/RlyehAD/mmic_md.git) using the [Gromacs](http://www.gromacs.org) software suite

## Preparing Input
```python
# Import moleucule and forcefield models
from mmelemental.models import Molecule, ForceField

# Import Strategy MD component
import mmic_md
# Import Tactic MD component 
import mmic_md_gmx

# Construct molecule and forcefield objects
# If a specific translator is impoted, it can be used with  
# mol = Molecule.from_file(path_to_file, TRANSLATOR_NAME)
mol = Molecule.from_file(path_to_file)
ff = ForceField.from_file(path_to_file)

# Construct input data model from molecule and forcefield objects
inp = mmic_md.InputMD(
	engine="gmx", # Engine must be gmx and must be specified
    schema_name=SCHEMA_NAME,
    schema_version=SCHEMA_VERSION,
    system={mol: ff},
    boundary=(
        "periodic",
        "periodic",
        "periodic",
        "periodic",
        "periodic",
        "periodic",
    ),
    max_steps=TOTAL_STEP_NUMBER,
    step_size=STEP_SIZE,
    method="md",
    freq_write={"nstxout": 5, "nstvout": 5, "nstenergy": 5, "nstlog": 5},
    long_forces={"method": METHOD_FOR_LONGRANGE_INTERACTION},
    short_forces={"method": METHOD_FOR_SHORT_INTERACTION},
    temp_couple={"method": T_COUPLE_METHOD, "ref_t": REFERENCE_T},
    press_couple={"method": P_COUPLE_METHOD},
)	
```

Examples for the Parameters:

*METHOD_FOR_LONGRANGE_INTERACTION*  "PME"

*METHOD_FOR_SHORT_INTERACTION*  "cut-off"

*T_COUPLE_METHOD*  "Berendsen"

*P_COUPLE_METHOD*  "Parrinello-Rahman"

## Runing MD Simulation
```python
# Import strategy compoent for runing MD simulation
from mmic_md_gmx.components import MDGMXComponent

# Run MD Simulation
outp = MDGMXComponent.compute(inp)
```

## Extracting Output
```python
# Extract the potential energy 
pot_energy = outp.observables["pot_energy"]
...
```


### Copyright

Copyright (c) 2021,  Xu Guo, Andrew Abi-Mansour


#### Acknowledgements
 
Project based on the 
[Computational Molecular Science Python Cookiecutter](https://github.com/molssi/cookiecutter-cms) version 0.0.
