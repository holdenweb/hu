import pytest
from hu import ObjectDict

NoneType = type(None)


@pytest.mark.parametrize(
    "typename, value",
    [("int", 42), ("float", 3.14159), ("string", "I'm a string"), ("NoneType", None)],
)
def test_passthrough(typename, value):
    assert ObjectDict(value) is value


def test_empty_list():
    value = ObjectDict([])
    assert type(value) is list
    assert value == []


def test_lists():
    list_1 = [1, 2, 3]
    od = ObjectDict(list_1)
    assert od == list_1
    for i1, i2 in zip(list_1, od):
        assert i1 is i2


def test_list_iteration():
    od = ObjectDict({"key1": [{"key": "value0"}, {"key": "value1"}, {"key": "value2"}]})
    assert (
        [o.key for o in od.key1]
        == [od.key1[i].key for i in range(3)]
        == [f"value{i}" for i in range(3)]
    )


def test_empty_object_dict():
    od_1 = ObjectDict({})
    assert type(od_1) is ObjectDict
    assert len(od_1) == 0


def test_object_dict():
    od_1 = ObjectDict({"top": "level"})
    assert type(od_1) is ObjectDict
    assert od_1.top == "level"
    od_1.new_string = "3456"
    assert set(od_1.keys()) == {"top", "new_string"}
    od_1.new_list = [1, 2, {"key": "value"}]
    assert type(od_1.new_list[2]) == ObjectDict
    assert od_1.new_list[2].key is od_1.new_list[2]["key"]
    assert od_1.new_list[2].key == "value"
    assert set(od_1.keys()) == {"top", "new_string", "new_list"}


def test_recursive_object_dict():
    od_1 = ObjectDict({"very": {"much": "smaller"}})
    assert od_1.very["much"] == "smaller"
    assert type(od_1.very) is ObjectDict, f"Wrong type: {type(od_1.very)}"


def test_absent_key_raises_correctly():
    od_1 = ObjectDict({"very": {"much": "smaller"}})
    with pytest.raises(AttributeError):
        _ = od_1.no_such_key
    with pytest.raises(KeyError):
        _ = od_1["no_such_key"]


def test_dir_method():
    od_1 = ObjectDict(dict(a=1, b=2, c=3, d=4))
    assert set(dir(od_1)) == set("abcd")


def test_no_args():
    assert dict(ObjectDict()) == {}


def test_invalid_value():
    with pytest.raises(ValueError):
        ObjectDict(object())


def test_generators():
    mydict = {"a": "b", "c": "d"}
    # This handles a generator in the same way a dict() does if it was passed
    # a dict generator
    od_1 = ObjectDict((k, v) for k, v in mydict.items())
    assert od_1 == mydict

    mylist = ["a", "b", "c", "d"]

    with pytest.raises(ValueError):
        # This errors in the same way as a dict() does if it was passed a list
        # generator
        ObjectDict(x for x in mylist)


def test_attribute_deletion():
    mydict = {"a": {"b": {"c": 1}}}
    od = ObjectDict(mydict)
    del od.a.b.c
    assert od == {"a": {"b": {}}}
    del od.a.b
    assert od == {"a": {}}
    del od.a
    assert od == {}


def test_item_deletion():
    #
    # Verify simple name deletion
    #
    mydict = {"a": {"b": [0, 1, 2, 3]}}
    od = ObjectDict(mydict)
    del od.a.b[2]
    assert od.a.b == [0, 1, 3]
    #
    # Verify we get an AttributeError deleting a non-existent name
    #
    with pytest.raises(AttributeError):
        del od.a.b.nosuch


if __name__ == "__main__":
    pytest.main()
