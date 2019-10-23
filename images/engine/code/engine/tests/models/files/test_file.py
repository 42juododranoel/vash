import string

import pytest

from engine.tests.conftest import (
    TEST_ROOT_FOLDER,
    FILE_CLASSES,
)


@pytest.fixture(params=FILE_CLASSES)
def model(request, monkeypatch):
    model = request.param
    monkeypatch.setattr(model, 'ROOT_FOLDER', TEST_ROOT_FOLDER, raising=True)
    return model


def test_create_creates_with_initial_content(model, path):
    file = model(path)
    file.create()
    assert file.is_present
    assert file.read() == file._get_initial_content()


def test_write_writes_when_created(model, path):
    file = model(path)
    file.create()
    assert file.is_present
    test_content = 'Test content'
    file.write(test_content)
    assert file.read() == test_content


def test_write_creates_and_writes_when_not_created(model, path):
    file = model(path)
    assert not file.is_present
    test_content = 'Test content'
    file.write(test_content)
    assert file.read() == test_content
