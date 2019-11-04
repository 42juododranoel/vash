import os

import pytest

from engine.tests.conftest import NODE_SUBCLASSES


@pytest.fixture(params=NODE_SUBCLASSES)
def model(request):
    return request.param


def test_has_root_folder(model, path):
    node = model(path)
    assert hasattr(node, 'ROOT_FOLDER')


def test_initialize_sets_path(model, path):
    node = model(path)
    assert node.path == path


def test_initialize_sets_name(model, path):
    node = model(path)
    assert node.name == path.split('/')[-1]


def test_absolute_path_with_absolute_path_as_path(model, absolute_path):
    node = model(absolute_path)
    assert node.absolute_path == absolute_path


def test_absolute_path_with_relative_path_as_path(model, relative_path):
    node = model(relative_path)
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


def test_create_creates_parent_folder(model):
    parent_path = 'parent'
    child_path = f'{parent_path}/node'
    node = model(child_path)
    parent_absolute_path = f'{model.ROOT_FOLDER}/{parent_path}'
    assert not os.path.isdir(parent_absolute_path)
    node.create()
    assert os.path.isdir(parent_absolute_path)


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
