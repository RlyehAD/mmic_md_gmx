# Import schema models for md simulation
from mmic_md.models import InputMD, OutputMD

# Import subcomponents for running md simulation with GMX
from .gmx_prep_component import PrepGmxComponent
from .gmx_compute_component import ComputeGmxComponent
from .gmx_post_component import PostGmxComponent

from mmic.components.blueprints import TacticComponent
from cmselemental.util.decorators import classproperty
from typing import Optional, Tuple, List, Any

__all__ = ["MDGmxComponent"]


class MDGmxComponent(TacticComponent):
    """Main entry component for running md simulation."""

    @classproperty
    def input(cls):
        return InputMD

    @classproperty
    def output(cls):
        return OutputMD

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
    ) -> Tuple[bool, OutputMD]:

        computeInput = PrepGmxComponent.compute(inputs)
        computeOutput = ComputeGmxComponent.compute(computeInput)
        OutputMD = PostGmxComponent.compute(computeOutput)
        return True, OutputMD

    def get_version(cls) -> str:
        """Finds program, extracts version, returns normalized version string.
        Returns
        -------
        str
            Return a valid, safe python version string.
        """
        raise NotImplementedError

    @classmethod
    def strategy_comps(cls) -> Any:
        """Returns the strategy component this (tactic) component belongs to.
        Returns
        -------
        Any
        """
        return set(mmic_md.components.MDComponent)
