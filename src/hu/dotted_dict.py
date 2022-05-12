import re

name_pat = r"(?P<name>[_A-Za-z][_A-Za-z0-9]*)"
subs_pat = r"\[(?P<index>-?\d*)\]"
first_pat = re.compile(rf"{name_pat}|{subs_pat}")
rest_pat = re.compile(rf"\.{name_pat}|{subs_pat}")


class DottedDict:
    """
    String subscripts are interpreted as keys to be used at successive
    layers of subscripting through the dictionaries and lists of a
    JSON-like record.

    Given a DottedDict with the following structure:

        dd = DottedDict({"first": {"second": [{}, {}, {"third": "bingo"}]}})

    the value returned by the expression

        dd['first.second[2].third']

    should be the string 'bingo'.
    """

    def __init__(self, d):
        self._d = d

    def _apply_key(self, o, k):
        try:
            return o[k]
        except ValueError:
            raise KeyError("Non-integer list subscript")
        except IndexError:
            raise KeyError('Invalid list index at end of "{}"'.format(k[: self.pos]))
        except KeyError:
            raise KeyError(
                'Unrecognised field name at end of "{}"'.format(k[: self.pos])
            )

    def __getitem__(self, key):
        """
        Returns the result of walking into the nested
        data structure using key as path specifier.
        """
        o = self._d
        for k in self._fragments(key):
            o = self._apply_key(o, k)
        return o

    def __setitem__(self, key, value):
        """
        Set the nested element located at the specified path key

        Currently handles only dicts.
        Does not recursively create missing structures
        """
        v = self._d
        fs = self._fragments(key)
        k = next(fs)
        for nk in fs:
            v = v[k]
            k = nk
        v[k] = value

    def __delitem__(self, key):
        """
        Delete the element indicated by the key string.
        """
        v = self._d
        fs = self._fragments(key)
        k = next(fs)
        for nk in fs:
            v = v[k]
            k = nk
        del v[nk]

    def _fragments(self, key):
        """
        Yield a sequence of key components:
        a string for attribute references and an
        integer for bracketed references.
        """
        self.pos, end = 0, len(key)
        pat = first_pat
        while self.pos < end:
            mo = pat.match(key, self.pos)
            if mo is None:
                raise KeyError(
                    "Cannot find name or list subscript at start of {!r}".format(
                        key[self.pos :]
                    )
                )
            s, i = mo.groups()
            self.pos = mo.end()
            if s:
                yield s
            else:
                yield int(i)
            pat = rest_pat
