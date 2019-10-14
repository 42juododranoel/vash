import json


def test_initial_content_is_json(created_json_file):
    initial_content = created_json_file._get_initial_content()
    assert isinstance(json.loads(initial_content), dict)
