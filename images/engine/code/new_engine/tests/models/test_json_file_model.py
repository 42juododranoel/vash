import json


class TestJsonFile:
    def test_initial_content_is_json(self, created_json_file):
        initial_content = created_json_file._get_initial_content()
        assert isinstance(json.loads(initial_content), dict)
