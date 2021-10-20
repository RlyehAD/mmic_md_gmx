from mmelemental.models.base import ProtoModel
from mmic_md.models import InputMD
from pydantic import Field


__all__ = ["OutputComputeGmx"]


class OutputComputeGmx(ProtoModel):
    proc_input: InputMD = Field(..., description="Procedure input schema.")
    molecule: str = Field(..., description="Molecule file string object")
    trajectory: str = Field(..., description="Trajectory file string object.")
    scratch_dir: str = Field(
        ..., description="The dir containing the traj file and the mold file"
    )
