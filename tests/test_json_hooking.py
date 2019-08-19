import json
import pytest
from hw.object_dict import ObjectDict

def test_recursive_object_build():
    data = """\
{"this": {"was": {"a": {"nested": "dictionary"}}}}"""
    od_1 = json.loads(data, object_hook=ObjectDict)
    assert type(od_1.this.was.a) is ObjectDict

def test_object_back_to_json():
    data = """\
{"this": {"was": {"a": {"nested": "dictionary"}}}}"""
    od_1 = json.loads(data, object_hook=ObjectDict)
    assert json.loads(json.dumps(od_1)) == {"this": {"was": {"a": {"nested": "dictionary"}}}}

if __name__ == '__main__':
    pytest.main()
