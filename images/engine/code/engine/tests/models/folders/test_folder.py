import os
import shutil

import pytest

from engine.tests.conftest import FOLDER_CLASSES


@pytest.fixture(params=FOLDER_CLASSES)
def model(request):
    return request.param


def test_is_empty_true_when_empty(model, path):
    folder = model(path)
    folder.create()
    for file in os.listdir(folder.absolute_path):
        try:
            os.remove(f'{folder.absolute_path}/{file}')
        except IsADirectoryError:
            shutil.rmtree(f'{folder.absolute_path}/{file}')

    assert folder.is_empty


def test_is_empty_false_when_not_empty(model, path):
    folder = model(path)
    folder.create()
    with open(f'{folder.absolute_path}/test.txt', 'w') as file:
        file.write('')
    assert not folder.is_empty


def test_create_creates_when_not_created(model, absolute_path):
    assert not os.path.isdir(absolute_path)
    model._create(absolute_path)
    assert os.path.isdir(absolute_path)


def test_create_fails_when_created(model, absolute_path):
    model._create(absolute_path)
    assert os.path.isdir(absolute_path)
    pytest.raises(FileExistsError, model._create, absolute_path)


def test_delete_deletes_when_created(model, absolute_path):
    model._create(absolute_path)
    assert os.path.isdir(absolute_path)
    model._delete(absolute_path)
    assert not os.path.isdir(absolute_path)


def test_delete_fails_when_not_created(model, absolute_path):
    assert not os.path.isdir(absolute_path)
    pytest.raises(FileNotFoundError, model._delete, absolute_path)


def test_check_presence_true_when_created(model, absolute_path):
    model._create(absolute_path)
    assert model._check_presence(absolute_path)


def test_check_presence_false_when_not_created(model, absolute_path):
    assert not model._check_presence(absolute_path)
