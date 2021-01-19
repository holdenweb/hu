# hu

[![CircleCI](https://circleci.com/gh/holdenweb/hu.svg?style=svg)](https://circleci.com/gh/holdenweb/hu "Build Status")
[![Dependabot Status](https://api.dependabot.com/badges/status?host=github&repo=holdenweb/hu)](https://dependabot.com)

Helpful utilities for open source developers

### hu.object_dict

Transforms a dict to allow attribute access to keys that conform with Python syntax
for names. Names that conflict with built-in dict attributes must be accessed using
subscripting as standard.

    from hu.object_dict import ObjectDict
    od = ObjectDict({"a": [{"first": "result"}]})
    assert od.a[0].first == "result"

### hu.dotted_dict

Allows access to dictionary-like structures using string keys whose components
can be attribute names or integer keys.

    from hu import DottedDict
    dd = DottedDict({"first": {"second": [{}, {}, {"third": "bingo"}]}})
    assert dd["first.second[2].third"] == "bingo"
