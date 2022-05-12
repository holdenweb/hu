import re


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
        for k in self._parse_path_key_spec(key):
            o = self._apply_key(o, k)
        return o

    def __setitem__(self, key, value):
        """
        Set the nested element located at the specified path key

        Currently handles only dicts.
        Does not recursively create missing structures
        """
        v = self._d
        fs = self._parse_path_key_spec(key)
        k = next(fs)
        for nk in fs:
            v = v[k]
            k = nk
        v[k] = value

    def __delitem__(self, key):
        """
        Delete the nested element located at the path key.
        """
        v = self._d
        fs = self._parse_path_key_spec(key)
        k = next(fs)
        for nk in fs:
            v = v[k]
            k = nk
        del v[nk]

    def _parse_path_key_spec(self, key):
        parser = KeySpecParser()
        for position, fragment in parser.parse(key):
            self.pos = position
            yield fragment


class KeySpecParser:
    IDENTIFIER_PATTERN = r"(?P<name>[_A-Za-z][_A-Za-z0-9]*)"
    SUBSCRIPT_PATTERN = r"\[(?P<index>-?\d*)\]"
    HEAD_PATTERN = re.compile(rf"{IDENTIFIER_PATTERN}|{SUBSCRIPT_PATTERN}")
    TAIL_PATTERN = re.compile(rf"\.{IDENTIFIER_PATTERN}|{SUBSCRIPT_PATTERN}")

    def parse(self, key):
        self._initialise_parser()
        end = len(key)
        while self.current_position < end:
            string, integer = self._next_token_match(key)
            if string:
                yield self.current_position, string
            else:
                yield self.current_position, int(integer)
            self.current_pattern = KeySpecParser.TAIL_PATTERN

    def _initialise_parser(self):
        self.current_position = 0
        self.current_pattern = KeySpecParser.HEAD_PATTERN

    def _next_token_match(self, key):
        pattern_match = self.current_pattern.match(key, self.current_position)
        self._raise_error_if_syntax_error(self.current_position, key, pattern_match)
        string, integer = pattern_match.groups()
        self.current_position = pattern_match.end()
        return string, integer

    def _raise_error_if_syntax_error(self, current_position, key, match):
        if match is None:
            raise KeyError(
                "Cannot find name or list subscript at start of {!r}".format(
                    key[current_position:]
                )
            )
