import pytest
from hw.object_dict import ObjectDict

def test_integer():
    # Verify integer pass-through
    value = 4567
    assert ObjectDict(value) is value


def test_string():
    # Verify string pass-through
    value = "4567"
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
    assert od_1.new_list[2].key is od_1.new_list[2]['key']
    assert od_1.new_list[2].key == "value"
    assert set(od_1.keys()) == {"top", "new_string", "new_list"}

def test_recursive_object_dict():
    od_1 = ObjectDict({'very': {'much': 'smaller'}})
    assert od_1.very['much'] == 'smaller'
    assert type(od_1.very) is ObjectDict, f"Wrong type: {type(od_1.very)}"


if __name__ == '__main__':
    pytest.main()
