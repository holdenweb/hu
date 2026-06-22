import pytest

from hu import DottedDict


@pytest.fixture
def dd():
    return DottedDict({"first": {"second": [{}, {}, {"third": "bingo"}]}})


@pytest.fixture
def odd_names():
    return DottedDict({})


def test_subscripts(dd):
    assert dd["first.second[2].third"] == "bingo"
    assert dd["first.second[-1].third"] == "bingo"


def fragments(dd, key):
    return [fragment for _position, fragment in dd._parse_path_key_spec(key)]


def test_fragments(dd):
    assert fragments(dd, "ab.cd[2][-1].ef.ij") == [
        "ab",
        "cd",
        2,
        -1,
        "ef",
        "ij",
    ]
    assert fragments(dd, "ab.cd[2].banana.ef.ij") == [
        "ab",
        "cd",
        2,
        "banana",
        "ef",
        "ij",
    ]


def test_exceptions(dd):
    with pytest.raises(KeyError):
        list(dd._parse_path_key_spec("ab.cd[2][banana].ef.ij"))


def test_out_of_range_list_index_raises_keyerror(dd):
    # Regression guard for the P3 refactor: an out-of-range list index must
    # surface as a KeyError naming the offending path, not leak a TypeError
    # from slicing an int fragment with shared parser state.
    with pytest.raises(KeyError) as exc_info:
        dd["first.second[99].third"]
    assert "first.second[99]" in str(exc_info.value)


def test_unknown_field_name_raises_keyerror(dd):
    with pytest.raises(KeyError) as exc_info:
        dd["first.nonesuch"]
    assert "first.nonesuch" in str(exc_info.value)


def test_deletion(dd):
    del dd["first.second[2].third"]
    assert dd["first.second"] == [{}, {}, {}]
    dd["first.second"] = [0, 1, 2]
    del dd["first.second[2]"]
    assert dd["first.second"] == [0, 1]


def test_single_fragment_deletion():
    # Regression guard: deleting a single-fragment key must not raise
    # UnboundLocalError (the loop body never runs, so __delitem__ must delete
    # the key bound by next(), not a loop variable).
    dd = DottedDict({"only": "value", "other": 1})
    del dd["only"]
    assert dd["other"] == 1
    with pytest.raises(KeyError):
        dd["only"]


def test_does_not_recursively_create_missing_structures():
    dd = DottedDict({"first": {"second": [{}, {}, {"third": "bingo"}]}})
    with pytest.raises(KeyError):
        dd["missing.element"] = None


def test_name_patterns(dd):
    for name in "_", "_12":
        assert fragments(dd, name) == [name]
