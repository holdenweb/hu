import re


class KeySpecParser:
    """
    Parse a path key spec such as "first.second[2].third" into a stream of
    (position, fragment) pairs, where fragment is an attribute name (str) or a
    list index (int) and position is the offset into the key just past the
    fragment (used to quote the path consumed so far in error messages).
    """

    IDENTIFIER_PATTERN = r"(?P<name>[_A-Za-z][_A-Za-z0-9]*)"
    SUBSCRIPT_PATTERN = r"\[(?P<index>-?\d*)\]"
    HEAD_PATTERN = re.compile(rf"{IDENTIFIER_PATTERN}|{SUBSCRIPT_PATTERN}")
    TAIL_PATTERN = re.compile(rf"\.{IDENTIFIER_PATTERN}|{SUBSCRIPT_PATTERN}")

    def parse(self, key):
        self._initialise_parser()
        end = len(key)
        while self.current_position < end:
            token = self._next_token_match(key)
            yield self.current_position, token

    def _initialise_parser(self):
        self.current_position = 0
        self.current_pattern = KeySpecParser.HEAD_PATTERN

    def _next_token_match(self, key):
        pattern_match = self.current_pattern.match(key, self.current_position)
        self._raise_error_if_syntax_error(key, pattern_match)
        self.current_position = pattern_match.end()
        self.current_pattern = KeySpecParser.TAIL_PATTERN
        return self._convert_to_token(pattern_match)

    def _convert_to_token(self, pattern_match):
        string, integer = pattern_match.groups()
        if string:
            return string
        return int(integer)

    def _raise_error_if_syntax_error(self, key, match):
        if match is None:
            raise KeyError(
                "Cannot find name or list subscript at start of {!r}".format(
                    key[self.current_position :]
                )
            )
