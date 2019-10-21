import pytest

from engine.tests.conftest import (
    NODE_SUBCLASSES,
    TEST_ROOT_FOLDER,
)


@pytest.fixture(params=NODE_SUBCLASSES)
def model(request, monkeypatch):
    model = request.param
    monkeypatch.setattr(model, 'ROOT_FOLDER', TEST_ROOT_FOLDER, raising=True)
    return model


def test_absolute_path_with_absolute_as_input(model, absolute_path):
    node = model(absolute_path)
    assert node.path == absolute_path
    assert node.absolute_path == absolute_path


def test_absolute_path_with_relative_as_input(model, relative_path):
    node = model(relative_path)
    assert node.path == relative_path
    assert node.absolute_path == f'{node.ROOT_FOLDER}/{relative_path}'


def test_is_present_true_when_created(model, path):
    node = model(path)
    assert not node.is_present
    node.create()
    assert node.is_present


def test_is_present_false_when_not_created(model, path):
    node = model(path)
    assert not node.is_present


def test_create_idles_when_created(model, path):
    node = model(path)
    assert not node.is_present
    node.create()
    assert node.is_present
    node.create()
    assert node.is_present


def test_create_creates_when_not_created(model, path):
    node = model(path)
    assert not node.is_present
    node.create()
    assert node.is_present


def test_delete_deletes_when_created(model, path):
    node = model(path)
    assert not node.is_present
    node.create()
    assert node.is_present
    node.delete()
    assert not node.is_present


def test_delete_idles_when_not_created(model, path):
    node = model(path)
    assert not node.is_present
    node.delete()
    assert not node.is_present
