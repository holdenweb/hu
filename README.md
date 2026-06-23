# hu

![Latest merge](https://github.com/holdenweb/hu/actions/workflows/lint.yaml/badge.svg?branch=main)

Helpful utilities for open source developers

## Installation

    uv add hu      # or: pip install hu

### hu.object_dict

`ObjectDict` gives nested dict/list data attribute-style access. It *wraps* the
data by composition (it is not a `dict` subclass) and wraps nested values lazily
on access, sharing the underlying structure — so reads, writes and deletes flow
straight through to the data you passed in.

    from hu import ObjectDict
    od = ObjectDict({"a": [{"first": "result"}]})
    assert od.a[0].first == "result"

Because it does not subclass `dict`, *every* key is reachable as an attribute —
including keys that would otherwise clash with dict methods such as `items`,
`keys` or `get`:

    od = ObjectDict({"items": [1, 2]})
    assert od.items == [1, 2]

Use `to_dict()` to recover a plain, detached `dict` (for example to serialise
with `json.dumps`):

    import json
    json.dumps(od.to_dict())

`ObjectDict` integrates with the `json` module as an `object_hook`:

    od = json.loads(text, object_hook=ObjectDict)

The same data is also reachable by path string through the `.path` accessor —
the path facade of the shared lazy core (see `hu.dotted_dict` below). Attribute
and path access read and write the one underlying structure:

    od = ObjectDict({"a": {"b": [1, 2]}})
    assert od.path["a.b[1]"] == 2
    od.path["a.b[1]"] = 9
    assert od.a.b[1] == 9
    assert od.path.get("a.missing", "fallback") == "fallback"

(`path` and `to_dict` are reserved attribute names; a data key called `"path"`
is reached with `od["path"]`.)

> If your data has a known, fixed shape, prefer a `dataclass` or a
> [pydantic](https://docs.pydantic.dev/) model: they give the same attribute
> access *plus* static type checking and editor completion, which
> attribute-access magic cannot. `ObjectDict` is for *dynamic* data whose shape
> you don't know ahead of time.

### hu.dotted_dict

`DottedDict` accesses dict/list structures using a single path string whose
components are attribute names or integer indices. It is the path facade of the
same lazy core as `ObjectDict` (equivalent to `ObjectDict(d).path`), so lookups
return lazily wrapped values that support attribute access in turn.

    from hu import DottedDict
    dd = DottedDict({"first": {"second": [{}, {}, {"third": "bingo"}]}})
    assert dd["first.second[2].third"] == "bingo"
    assert dd["first.second[2]"].third == "bingo"

It also supports `get` (with an optional default) and membership tests; any path
that does not resolve yields the default / `False` rather than raising:

    assert dd.get("first.second[2].third") == "bingo"
    assert dd.get("first.missing", "fallback") == "fallback"
    assert "first.second[2].third" in dd
