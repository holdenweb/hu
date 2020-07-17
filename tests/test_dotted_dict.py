import pytest
from hu import DottedDict
from hu.dotted_dict import first_pat
from hu.dotted_dict import name_pat
from hu.dotted_dict import rest_pat
from hu.dotted_dict import subs_pat


@pytest.fixture
def dd():
    return DottedDict({"first": {"second": [{}, {}, {"third": "bingo"}]}})


@pytest.fixture
def odd_names():
    return DottedDict({})


def test_subscripts(dd):
    assert dd["first.second[2].third"] == "bingo"
    assert dd["first.second[-1].third"] == "bingo"


def test_fragments(dd):
    assert list(dd._fragments("ab.cd[2][-1].ef.ij")) == ["ab", "cd", 2, -1, "ef", "ij"]
    assert list(dd._fragments("ab.cd[2].banana.ef.ij")) == [
        "ab",
        "cd",
        2,
        "banana",
        "ef",
        "ij",
    ]


def test_exceptions(dd):
    with pytest.raises(KeyError):
        list(dd._fragments("ab.cd[2][banana].ef.ij")) == [
            "ab",
            "cd",
            2,
            "banana",
            "ef",
            "ij",
        ]


def test_name_patterns(dd):
    for name in "_", "_12":
        assert list(dd._fragments(name)) == [name]
