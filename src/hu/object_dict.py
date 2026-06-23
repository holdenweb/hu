from collections.abc import MutableSequence


def _wrap(value):
    """
    Wrap dicts and lists for attribute/element access; pass scalars through.

    Wrapping is lazy and shares the underlying container, so wrappers stay in
    sync with the data they view and writes propagate back to it.
    """
    if isinstance(value, (ObjectDict, ObjectList)):
        return value
    if isinstance(value, dict):
        return ObjectDict(value)
    if isinstance(value, list):
        return ObjectList(value)
    return value


def _unwrap(value):
    """Return the plain container backing a wrapper, so stored data stays plain."""
    if isinstance(value, (ObjectDict, ObjectList)):
        return value._data
    return value


def _to_plain(value):
    """Recursively convert wrappers and their contents to plain dicts/lists."""
    if isinstance(value, (ObjectDict, ObjectList)):
        value = value._data
    if isinstance(value, dict):
        return {k: _to_plain(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_to_plain(v) for v in value]
    return value


class ObjectDict:
    """
    A lazy attribute-access view over a dict-like structure.

    ObjectDict wraps a dict by composition rather than subclassing it, so every
    key -- including ones that clash with dict method names such as ``items`` or
    ``keys`` -- is reachable as an attribute. Nested dicts and lists are wrapped
    on access (not copied up front), and the wrapper shares the underlying data,
    so mutations are visible in both directions::

        od = ObjectDict({"a": [{"b": "c"}]})
        assert od.a[0].b == "c"

    Use :meth:`to_dict` to recover a plain, detached ``dict`` (for example to
    pass to ``json.dumps``). For data with a known, fixed shape a dataclass or a
    pydantic model is usually a better fit, since those give the same attribute
    access *plus* static typing and editor completion, which attribute-access
    magic cannot.
    """

    def __init__(self, data=None):
        if data is None:
            data = {}
        elif isinstance(data, ObjectDict):
            data = data._data
        elif not isinstance(data, dict):
            data = dict(data)  # a mapping or iterable of pairs, like dict() itself
        object.__setattr__(self, "_data", data)

    # -- attribute access ---------------------------------------------------

    def __getattr__(self, name):
        if name == "_data":  # guard against recursion if _data is missing
            raise AttributeError(name)
        try:
            return _wrap(self._data[name])
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        if name == "_data":
            object.__setattr__(self, name, value)
        else:
            self._data[name] = _unwrap(value)

    def __delattr__(self, name):
        try:
            del self._data[name]
        except KeyError:
            raise AttributeError(name)

    def __dir__(self):
        return sorted(self._data)

    # -- item access --------------------------------------------------------

    def __getitem__(self, key):
        return _wrap(self._data[key])

    def __setitem__(self, key, value):
        self._data[key] = _unwrap(value)

    def __delitem__(self, key):
        del self._data[key]

    def __contains__(self, key):
        return key in self._data

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    # -- equality / display / conversion ------------------------------------

    def __eq__(self, other):
        if isinstance(other, ObjectDict):
            other = other._data
        return self._data == other

    def __repr__(self):
        return f"ObjectDict({self._data!r})"

    def to_dict(self):
        """Return a plain, detached ``dict`` copy of the wrapped data."""
        return _to_plain(self)


class ObjectList(MutableSequence):
    """
    A lazy element-wrapping view over a list, the companion to ObjectDict.

    Elements are wrapped on access so nested dicts keep their attribute access,
    and the wrapper shares the underlying list so mutations write through. The
    full mutable-sequence API (append, extend, insert, pop, ...) comes from
    MutableSequence on top of the methods defined here.
    """

    def __init__(self, data):
        self._data = data

    def __getitem__(self, index):
        if isinstance(index, slice):
            return ObjectList(self._data[index])
        return _wrap(self._data[index])

    def __setitem__(self, index, value):
        self._data[index] = _unwrap(value)

    def __delitem__(self, index):
        del self._data[index]

    def __len__(self):
        return len(self._data)

    def insert(self, index, value):
        self._data.insert(index, _unwrap(value))

    def __eq__(self, other):
        if isinstance(other, ObjectList):
            other = other._data
        return self._data == other

    def __repr__(self):
        return f"ObjectList({self._data!r})"

    def to_list(self):
        """Return a plain, detached ``list`` copy of the wrapped data."""
        return _to_plain(self)
