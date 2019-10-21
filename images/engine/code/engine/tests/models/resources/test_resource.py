import pytest

from engine.tests.conftest import (
    RESOURCE_CLASSES,
    TEST_ROOT_FOLDER,
)


@pytest.fixture(params=RESOURCE_CLASSES)
def model(request, monkeypatch):
    model = request.param
    resource_root_folder = model.ROOT_FOLDER
    monkeypatch.setattr(
        model,
        'ROOT_FOLDER',
        f'{TEST_ROOT_FOLDER}{resource_root_folder}',
        raising=True
    )
    return model


def test_create_creates_files(model, path):
    resource = model(path)
    assert not resource.is_present
    resource.create()
    for _, file in resource.files.items():
        assert file.is_present
