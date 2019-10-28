import pytest

from engine.tests.conftest import RESOURCE_CLASSES


@pytest.fixture(params=RESOURCE_CLASSES)
def model(request, capybara_patch):
    return capybara_patch(request.param)


def test_initialize_sets_files(model, path):
    resource = model(path)
    assert hasattr(resource, 'files')


def test_get_files_returns_mapping(model, path):
    resource = model(path)
    assert isinstance(resource._get_files(), dict)


def test_create_also_creates_files(model, path):
    resource = model(path)
    assert not resource.is_present
    resource.create()
    for _, file in resource.files.items():
        assert file.is_present
