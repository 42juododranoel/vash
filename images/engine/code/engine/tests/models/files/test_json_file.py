# import json
#
# import pytest
#
# from engine.tests.conftest import (
#     JSON_FILE_AND_SUBCLASSES,
#     TEST_ROOT_FOLDER
# )
#
#
# @pytest.fixture(params=JSON_FILE_AND_SUBCLASSES)
# def model(request, monkeypatch):
#     model = request.param
#     monkeypatch.setattr(model, 'ROOT_FOLDER', TEST_ROOT_FOLDER, raising=True)
#     return model
#
#
# def test_initial_content_is_json(model, path):
#     json_file = model(path)
#     initial_content = json_file._get_initial_content()
#     assert isinstance(json.loads(initial_content), dict)
