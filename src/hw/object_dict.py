NoneType = type(None)


class ObjectDict(dict):
    """
    Makes a dictionary behave like an object, with attribute-style access.
    """

    sentinel = object()  # Unique instance that cannot be passed as an argument

    def __new__(cls, arg=sentinel):
        """
        This recursive dict subclass converts a dict into an ObjectDict,
        which can use attribute access to retrieve and set keys.
        Floats, ints, strings, None and existing ObjectDicts are simply
        returned. Lists are transformed into lists of ObjectDicts.
        The __init__ method will only be called for ObjectDicts,
        since only then is the argument class is the same as the returned
        value. When a dict is passed in, object creation is delegated to
        the superclass, and its contents are initialised in __init__.
        """
        if arg is cls.sentinel:
            return super().__new__(cls)
        elif isinstance(arg, (int, float, str, ObjectDict, NoneType)):
            return arg
        elif isinstance(arg, list):
            return list(ObjectDict(x) for x in arg)
        elif isinstance(arg, dict):
            return super().__new__(cls, arg)
        else:
            raise ValueError(f"{type(arg)} objects cannot be ObjectDicts")

    def __init__(self, arg=sentinel):
        """
        This method is only called after __new__ returns an ObjectDict
        instance. The __init__ method actually initialises the values
        in the underlying dict.
        """
        if type(arg) is ObjectDict:
            return  # Assume existing ObjectDicts do not need re-initialising
        if arg is self.sentinel:  # Called without args
            arg = {}
        for (k, v) in arg.items():
            self[k] = ObjectDict(v)

    def __getattr__(self, name: str):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        value = ObjectDict(value)
        super().__setitem__(name, value)

    def __dir__(self):
        return sorted(self.keys())
