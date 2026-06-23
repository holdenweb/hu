from importlib import metadata

from .dotted_dict import DottedDict
from .object_dict import ObjectDict, ObjectList

__all__ = ("__version__", "DottedDict", "ObjectDict", "ObjectList")

__version__ = metadata.version("hu")
