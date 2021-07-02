""" Populate this file if your component requires its own models """

from mmelemental.models.base import ProtoModel

__all__ = ["InputModel", "OutputModel"]


class InputModel(ProtoModel):
    """ An input model for mmic_md_gmx. """

    ...


class OutputModel(ProtoModel):
    """ An output model for mmic_md_gmx. """

    ...
