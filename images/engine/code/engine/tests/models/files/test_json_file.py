import pytest

from engine.tests.conftest import JSON_FILE_SUBCLASSES


@pytest.fixture(params=JSON_FILE_SUBCLASSES)
def model(request):
    return request.param


def test_initial_content_is_dictionary(model, path):
    json_file = model(path)
    initial_content = json_file._get_initial_content()
    assert isinstance(initial_content, dict)


def test_setitem_writes_to_file(model, path):
    json_file = model(path)
    json_file.create()
    test_key = 'key'
    test_value = 'value'
    json_file[test_key] = test_value
    assert test_key in json_file.read()


def test_setitem_creates_when_not_created(model, path):
    json_file = model(path)
    test_key = 'key'
    test_value = 'value'
    json_file[test_key] = test_value
    assert json_file.is_created


def test_getitem_raises_key_error_when_key_is_not_set(model, path):
    json_file = model(path)
    json_file.create()
    test_key = 'key'
    pytest.raises(KeyError, json_file.__getitem__, test_key)


def test_getitem_works_when_key_is_set(model, path):
    json_file = model(path)
    json_file.create()
    test_key = 'key'
    test_value = 'value'
    json_file[test_key] = test_value
    assert json_file[test_key] == test_value
