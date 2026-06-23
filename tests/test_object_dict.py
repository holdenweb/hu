import pytest

from hu import ObjectDict, ObjectList

# --- construction -----------------------------------------------------------


def test_empty_object_dict():
    od = ObjectDict({})
    assert type(od) is ObjectDict
    assert len(od) == 0


def test_no_args():
    assert ObjectDict().to_dict() == {}


def test_accepts_generator_of_pairs():
    mydict = {"a": "b", "c": "d"}
    # A generator of pairs is accepted, exactly as dict() would accept it.
    od = ObjectDict((k, v) for k, v in mydict.items())
    assert od == mydict


def test_generator_of_non_pairs_is_rejected():
    # Fails the same way dict() does when handed a non-pair iterable.
    with pytest.raises(ValueError):
        ObjectDict(x for x in ["a", "b", "c", "d"])


def test_non_mapping_argument_is_rejected():
    with pytest.raises(TypeError):
        ObjectDict(object())


def test_wrapping_an_object_dict_shares_its_data():
    inner = ObjectDict({"a": 1})
    outer = ObjectDict(inner)
    outer.a = 2
    assert inner.a == 2


# --- attribute access -------------------------------------------------------


def test_attribute_access():
    od = ObjectDict({"top": "level"})
    assert od.top == "level"


def test_scalar_values_pass_through_unwrapped():
    od = ObjectDict({"i": 42, "f": 3.14, "s": "x", "n": None})
    assert od.i == 42 and type(od.i) is int
    assert od.f == 3.14
    assert od.s == "x"
    assert od.n is None


def test_recursive_attribute_access():
    od = ObjectDict({"very": {"much": "smaller"}})
    assert type(od.very) is ObjectDict
    assert od.very.much == "smaller"
    assert od.very["much"] == "smaller"


def test_absent_key_raises_correctly():
    od = ObjectDict({"very": {"much": "smaller"}})
    with pytest.raises(AttributeError):
        _ = od.no_such_key
    with pytest.raises(KeyError):
        _ = od["no_such_key"]


def test_dir_lists_keys():
    od = ObjectDict(dict(a=1, b=2, c=3, d=4))
    assert set(dir(od)) == set("abcd")


def test_iter_and_contains_and_len():
    od = ObjectDict({"a": 1, "b": 2})
    assert set(od) == {"a", "b"}
    assert "a" in od
    assert "z" not in od
    assert len(od) == 2


# --- the composition payoff: data keys never collide with method names ------


def test_keys_named_like_dict_methods_are_accessible():
    # A data key called "items"/"keys"/"get" must be real data reachable as an
    # attribute, not a shadowed dict method.
    od = ObjectDict({"items": [1, 2], "keys": "k", "get": 0})
    assert od.items == [1, 2]
    assert od.keys == "k"
    assert od.get == 0


# --- lists ------------------------------------------------------------------


def test_list_values_are_wrapped_lazily():
    od = ObjectDict({"key1": [{"key": "value0"}, {"key": "value1"}]})
    assert type(od.key1) is ObjectList
    assert [o.key for o in od.key1] == ["value0", "value1"]
    assert od.key1[1].key == "value1"
    assert type(od.key1[0]) is ObjectDict


def test_list_equality_against_plain_list():
    od = ObjectDict({"xs": [1, 2, 3]})
    assert od.xs == [1, 2, 3]


def test_setattr_list_then_indexed_access():
    od = ObjectDict({})
    od.new_list = [1, 2, {"key": "value"}]
    assert type(od.new_list[2]) is ObjectDict
    assert od.new_list[2].key == "value"


# --- the invariant the old eager dict-subclass design could not hold --------


def test_setitem_wraps_on_access():
    # Item assignment must wrap on access, just like attribute assignment.
    od = ObjectDict({})
    od["new"] = {"nested": 1}
    assert type(od.new) is ObjectDict
    assert od.new.nested == 1


def test_setattr_then_access():
    od = ObjectDict({})
    od.new = {"nested": 1}
    assert od.new.nested == 1


def test_nested_assignment_persists():
    od = ObjectDict({"a": {}})
    od.a.b = {"c": 1}
    assert od.a.b.c == 1
    assert od.to_dict() == {"a": {"b": {"c": 1}}}


def test_changes_to_backing_data_are_seen():
    # The wrapper is a lazy view, so mutating the underlying data after
    # construction is visible through the wrapper.
    backing = {"a": {"b": 1}}
    od = ObjectDict(backing)
    backing["a"]["c"] = 2
    assert od.a.c == 2


def test_list_mutation_writes_through():
    od = ObjectDict({"xs": [{"k": 0}]})
    od.xs.append({"k": 1})
    assert od.xs[1].k == 1
    assert od.to_dict() == {"xs": [{"k": 0}, {"k": 1}]}


# --- deletion ---------------------------------------------------------------


def test_attribute_deletion():
    od = ObjectDict({"a": {"b": {"c": 1}}})
    del od.a.b.c
    assert od == {"a": {"b": {}}}
    del od.a.b
    assert od == {"a": {}}
    del od.a
    assert od == {}


def test_item_deletion():
    od = ObjectDict({"a": {"b": [0, 1, 2, 3]}})
    del od.a.b[2]
    assert od.a.b == [0, 1, 3]
    # Deleting a non-existent name on a wrapped list raises AttributeError.
    with pytest.raises(AttributeError):
        del od.a.b.nosuch


def test_delattr_missing_attribute_raises():
    # Regression guard: __delattr__ must *raise* AttributeError for a missing
    # attribute, not merely construct and return one (which silently does
    # nothing).
    od = ObjectDict({"present": 1})
    with pytest.raises(AttributeError):
        del od.absent


# --- conversion -------------------------------------------------------------


def test_to_dict_returns_plain_nested_structure():
    data = {"a": {"b": [{"c": 1}]}}
    od = ObjectDict(data)
    plain = od.to_dict()
    assert type(plain) is dict
    assert type(plain["a"]) is dict
    assert type(plain["a"]["b"]) is list
    assert type(plain["a"]["b"][0]) is dict
    assert plain == data


def test_to_dict_is_detached_from_the_wrapper():
    data = {"a": {"b": 1}}
    od = ObjectDict(data)
    snapshot = od.to_dict()
    od.a.b = 99
    assert snapshot["a"]["b"] == 1


# --- path-string access via the shared lazy core ----------------------------


def test_path_get_returns_wrapped_value():
    od = ObjectDict({"a": {"b": [{"c": "deep"}]}})
    assert od.path["a.b[0].c"] == "deep"
    assert type(od.path["a.b[0]"]) is ObjectDict


def test_path_and_attribute_access_share_backing():
    od = ObjectDict({"a": {"b": 1}})
    od.path["a.b"] = 2
    assert od.a.b == 2
    od.a.b = 3
    assert od.path["a.b"] == 3


def test_path_get_default_and_membership():
    od = ObjectDict({"a": {"b": 1}})
    assert od.path.get("a.b") == 1
    assert od.path.get("a.x", "default") == "default"
    assert "a.b" in od.path
    assert "a.x" not in od.path


def test_path_delete():
    od = ObjectDict({"a": {"b": 1, "c": 2}})
    del od.path["a.b"]
    assert od.to_dict() == {"a": {"c": 2}}


def test_path_on_object_list():
    ol = ObjectList([{"a": 1}, {"a": 2}])
    assert ol.path["[1].a"] == 2


def test_path_is_reserved_but_key_reachable_by_subscript():
    od = ObjectDict({"path": "/tmp"})
    assert not isinstance(od.path, str)  # the .path accessor shadows the key
    assert od["path"] == "/tmp"  # ...but the data is still reachable


if __name__ == "__main__":
    pytest.main()
