# hu

[![CircleCI](https://circleci.com/gh/holdenweb/hu.svg?style=svg)](https://circleci.com/gh/holdenweb/hu "Build Status")

Helpful utilities for open source developers

### hu.object_dict

Transforms a dict to allow attribute access to keys that conform with Python syntax
for names. Names that conflict with built-in dict attributes must be accessed using
subscripting as standard.

    from hu import ObjectDict
    od = ObjectDict({"a": [{"first": "result"}]})
    assert od.a[0].first == "result"
