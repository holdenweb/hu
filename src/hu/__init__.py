from importlib import metadata

from .dotted_dict import DottedDict
from .object_dict import ObjectDict

__all__ = ("__version__", "DottedDict", "ObjectDict")

__version__ = metadata.version("hu")
