import json

import pytest

from hu import ObjectDict


def test_recursive_object_build():
    data = """\
{"this": {"was": {"a": {"nested": ["dictionary"]}}}}"""
    od_1 = json.loads(data, object_hook=ObjectDict)
    assert type(od_1.this.was.a) is ObjectDict


def test_object_back_to_json():
    data = {"this": {"was": {"a": {"nested": ["dictionary"]}}}}
    json_data = json.dumps(data)
    od_1 = json.loads(json_data, object_hook=ObjectDict)
    assert type(od_1) is ObjectDict
    # ObjectDict is not itself a dict, so round-trip via to_dict().
    assert json.loads(json.dumps(od_1.to_dict())) == data


if __name__ == "__main__":
    pytest.main()
