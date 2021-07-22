from mmelemental.models.base import ProtoModel
from mmic_md.models import MDInput
from pydantic import Field


__all__ = ["ComputeGmxOutput"]


class ComputeGmxOutput(ProtoModel):
    proc_input: MDInput = Field(..., description="Procedure input schema.")
    molecule: str = Field(..., description="Molecule file string object")
    trajectory: str = Field(..., description="Trajectory file string object.")
    scratch_dir: str = Field(
        ..., description="The dir containing the traj file and the mold file"
    )
