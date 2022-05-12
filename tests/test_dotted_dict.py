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


def test_deletion(dd):
    del dd["first.second[2].third"]
    assert dd["first.second"] == [{}, {}, {}]
    dd["first.second"] = [0, 1, 2]
    del dd["first.second[2]"]
    assert dd["first.second"] == [0, 1]


def test_name_patterns(dd):
    for name in "_", "_12":
        assert list(dd._fragments(name)) == [name]
