import pytest

from engine.tests.conftest import FILE_AND_SUBCLASSES

# TODO: test write writes content
# TODO: test write writes binary content
# TODO: test read reads content
# TODO: test read reads binary content


@pytest.mark.parametrize('model', FILE_AND_SUBCLASSES)
def test_create_creates_with_initial_content(create, model, file_path):
    file = create(model, file_path)
    with open(file.path) as file_on_disk:
        assert file_on_disk.read() == file._get_initial_content()


@pytest.mark.parametrize('model', FILE_AND_SUBCLASSES)
def test_write_writes_when_present(create, model, file_path):
    file = create(model, file_path)
    test_content = 'Test content'
    file.write(test_content)
    with open(file.path) as file_on_disk:
        assert file_on_disk.read() == test_content


@pytest.mark.parametrize('model', FILE_AND_SUBCLASSES)
def test_write_creates_and_writes_when_missing(model, file_path):
    file = model(file_path)
    test_content = 'Test content'
    file.write(test_content)
    with open(file.path) as file_on_disk:
        assert file_on_disk.read() == test_content
