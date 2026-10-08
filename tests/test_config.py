from legalease.config import deep_merge


def test_deep_merge_keeps_nested_defaults():
    merged = deep_merge({"a": {"b": 1, "c": 2}}, {"a": {"b": 3}})
    assert merged == {"a": {"b": 3, "c": 2}}
