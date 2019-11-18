import pytest

from engine.tests.conftest import RESOURCE_CLASSES


@pytest.fixture(params=RESOURCE_CLASSES)
def model(request):
    return request.param


def test_initialize_sets_files(model, path):
    resource = model(path)
    assert hasattr(resource, 'files')


def test_files_returns_dictionary(model, path):
    resource = model(path)
    assert isinstance(resource.files, dict)


def test_create_also_creates_files(model, path):
    resource = model(path)
    assert not resource.is_created
    resource.create()
    for _, file in resource.files.items():
        assert file.is_created
