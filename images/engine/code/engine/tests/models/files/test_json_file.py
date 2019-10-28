import pytest

from engine.tests.conftest import JSON_FILE_SUBCLASSES


@pytest.fixture(params=JSON_FILE_SUBCLASSES)
def model(request, capybara_patch):
    return capybara_patch(request.param)


def test_initial_content_is_dictionary(model, path):
    json_file = model(path)
    initial_content = json_file._get_initial_content()
    assert isinstance(initial_content, dict)
