import pytest

from engine.tests.conftest import (
    TEST_ROOT_FOLDER,
    FOLDER_CLASSES
)


@pytest.fixture(params=FOLDER_CLASSES)
def model(request, monkeypatch):
    model = request.param
    monkeypatch.setattr(model, 'ROOT_FOLDER', TEST_ROOT_FOLDER, raising=True)
    return model


def test_is_empty_false_when_populated(model, path):
    folder = model(path)
    folder.create()
    with open(f'{folder.absolute_path}/test.txt', 'w') as file:
        file.write('')
    assert not folder.is_empty
