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
    with open(file.absolute_path) as file_on_disk:
        assert file_on_disk.read() == file._get_initial_content()


def test_write_writes_when_present(model, path):
    file = model(path)
    file.create()
    assert file.is_present
    test_content = 'Test content'
    file.write(test_content)
    with open(file.absolute_path) as file_on_disk:
        assert file_on_disk.read() == test_content


def test_write_creates_and_writes_when_missing(model, path):
    file = model(path)
    test_content = 'Test content'
    file.write(test_content)
    with open(file.absolute_path) as file_on_disk:
        assert file_on_disk.read() == test_content


def test_write_writes_plain_content(model, path):
    file = model(path)
    file.create()
    test_content = string.ascii_letters + string.punctuation
    file.write(test_content)
    with open(file.absolute_path) as file_on_disk:
        assert file_on_disk.read() == test_content


def test_write_writes_binary_content(model, path):
    file = model(path)
    file.create()
    test_content = bytes(string.ascii_letters + string.punctuation, 'utf8')
    file.write(test_content)
    with open(file.absolute_path, 'rb') as file_on_disk:
        assert file_on_disk.read() == test_content


def test_read_reads_plain_content(model, path):
    file = model(path)
    file.create()
    test_content = string.ascii_letters + string.punctuation
    with open(file.absolute_path, 'w') as file_on_disk:
        file_on_disk.write(test_content)
    assert file.read() == test_content


def test_read_reads_binary_content(model, path):
    file = model(path)
    file.create()
    test_content = bytes(string.ascii_letters + string.punctuation, 'utf8')
    with open(file.absolute_path, 'wb') as file_on_disk:
        file_on_disk.write(test_content)
    assert file.read(is_binary=True) == test_content
