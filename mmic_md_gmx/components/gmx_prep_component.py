# Import models
from mmic_md.models.input import InputMD
from mmic_md_gmx.models import InputComputeGmx

# Import components
from mmic_cmd.components import CmdComponent
from mmic.components.blueprints import GenericComponent
from cmselemental.util.decorators import classproperty

from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional
import os
import tempfile

__all__ = ["PrepGmxComponent"]
_supported_solvents = ("spc", "tip3p", "tip4p")  # This line may be delete later


class PrepGmxComponent(GenericComponent):
    """
    Prepares input for running molecular dynamics simulations using GMX engine.
    The Molecule object from MMIC schema will be
    converted to a .pdb file here then converted to a .gro file.
    .mdp and .top files will also be constructed
    according to the info in MMIC schema.
    """

    @classproperty
    def input(cls):
        return InputMD

    @classproperty
    def output(cls):
        return InputComputeGmx

    @classproperty
    def version(cls) -> str:
        """Finds program, extracts version, returns normalized version string.
        Returns
        -------
        str
            Return a valid, safe python version string.
        """
        return ""

    def execute(
        self,
        inputs: InputMD,
        extra_outfiles: Optional[List[str]] = None,
        extra_commands: Optional[List[str]] = None,
        scratch_name: Optional[str] = None,
        timeout: Optional[int] = None,
    ) -> Tuple[bool, InputComputeGmx]:

        if isinstance(inputs, dict):
            inputs = self.input(**inputs)

        # Start to build mdp file dict
        mdp_inputs = {
            "integrator": inputs.method,
            "dt": inputs.step_size,
            "nsteps": inputs.max_steps,
            "coulombtype": inputs.long_forces.method,
            "vdw-type": inputs.short_forces.method,
            "pbc": inputs.boundary,
        }

        # Extract output setup from freq_write dict
        for key, val in inputs.freq_write.items():
            mdp_inputs[key] = val

        # Extract T couple and P couple setup
        for key, val in inputs.temp_couple.items():
            mdp_inputs[key] = val

        for key, val in inputs.press_couple.items():
            mdp_inputs[key] = val

        # Translate boundary str tuple (perodic,perodic,perodic) to a string e.g. xyz
        pbc_dict = dict(zip(["x", "y", "z"], list(mdp_inputs["pbc"])))
        pbc = ""
        for dim in list(pbc_dict.keys()):
            if pbc_dict[dim] != "periodic":
                continue
            else:
                pbc = pbc + dim  # pbc is a str, may need to be initiated elsewhere
        mdp_inputs["pbc"] = pbc

        # Write .mdp file
        mdp_file = tempfile.NamedTemporaryFile(suffix=".mdp", delete=False)
        with open(mdp_file.name, "w") as inp:
            for key, val in mdp_inputs.items():
                inp.write(f"{key} = {val}\n")

        """
        fs = inputs.forcefield
        mols = inputs.molecule

        ff_name, ff = list(
            fs.items()
        ).pop()  # Here ff_name gets actually the related mol name, but it will not be used
        mol_name, mol = list(mols.items()).pop()
        """

        mol, ff = list(inputs.system.items()).pop()

        gro_file = tempfile.NamedTemporaryFile(suffix=".gro", delete=False)  # output gro
        top_file = tempfile.NamedTemporaryFile(suffix=".top", delete=False)
        boxed_gro_file = tempfile.NamedTemporaryFile(suffix=".gro", delete=False)

        mol.to_file(gro_file.name, translator="mmic_parmed")
        ff.to_file(top_file.name, translator="mmic_parmed")

        input_model = {
            "gro_file": gro_file.name,
            "proc_input": inputs,
            "boxed_gro_file": boxed_gro_file.name,
        }
        clean_files, cmd_input = self.build_input(input_model)
        rvalue = CmdComponent.compute(cmd_input)

        scratch_dir = str(rvalue.scratch_directory)
        self.cleanup(clean_files)  # Del the gro in the working dir

        gmx_compute = InputComputeGmx(
            proc_input=inputs,
            mdp_file=mdp_file.name,
            forcefield=top_file.name,
            molecule=boxed_gro_file.name,
            scratch_dir=scratch_dir,
            schema_name=inputs.schema_name,
            schema_version=inputs.schema_version,
        )

        return True, gmx_compute

    @staticmethod
    def cleanup(remove: List[str]):
        for item in remove:
            if os.path.isdir(item):
                shutil.rmtree(item)
            elif os.path.isfile(item):
                os.remove(item)

    def build_input(
        self,
        inputs: Dict[str, Any],
        config: Optional["TaskConfig"] = None,
        template: Optional[str] = None,
    ) -> Dict[str, Any]:

        assert inputs["proc_input"].engine == "gmx", "Engine must be gmx (Gromacs)!"
        clean_files = []

        boxed_gro_file = inputs["boxed_gro_file"]
        clean_files.append(inputs["gro_file"])

        env = os.environ.copy()

        if config:
            env["MKL_NUM_THREADS"] = str(config.ncores)
            env["OMP_NUM_THREADS"] = str(config.ncores)

        scratch_directory = config.scratch_directory if config else None

        cmd = [
            inputs["proc_input"].engine,
            "editconf",
            "-f",
            inputs["gro_file"],
            "-d",
            "2",
            "-o",
            boxed_gro_file,
        ]
        outfiles = [boxed_gro_file]

        return (
            clean_files,
            {
                "command": cmd,
                "infiles": [inputs["gro_file"]],
                "outfiles": outfiles,
                "outfiles_track": outfiles,
                "scratch_directory": scratch_directory,
                "environment": env,
                "scratch_messy": True,
            },
        )
