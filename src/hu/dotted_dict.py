from ._keyspec import KeySpecParser
from .object_dict import _PathView

__all__ = ["DottedDict", "KeySpecParser"]


class DottedDict:
    """
    Path-string access to nested dict/list structures.

    String subscripts are interpreted as keys to be used at successive layers
    of subscripting through the dictionaries and lists of a JSON-like record::

        dd = DottedDict({"first": {"second": [{}, {}, {"third": "bingo"}]}})
        assert dd["first.second[2].third"] == "bingo"

    DottedDict is the path facade of the shared lazy core: lookups return lazily
    wrapped values, so a result supports attribute access in turn
    (``dd["first.second[2]"].third``). ``ObjectDict(d).path`` offers the same
    access over an attribute-first wrapper.
    """

    def __init__(self, d):
        self._d = d

    def _view(self):
        return _PathView(self._d)

    def __getitem__(self, key):
        return self._view()[key]

    def __setitem__(self, key, value):
        self._view()[key] = value

    def __delitem__(self, key):
        del self._view()[key]

    def get(self, key, default=None):
        return self._view().get(key, default)

    def __contains__(self, key):
        return key in self._view()

    def _parse_path_key_spec(self, key):
        yield from KeySpecParser().parse(key)
