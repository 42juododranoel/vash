import pytest

from engine.models.files.meta_file import MetaFile
from engine.tests.conftest import TEST_ROOT_FOLDER


@pytest.fixture
def model(request, monkeypatch):
    model = MetaFile
    monkeypatch.setattr(model, 'ROOT_FOLDER', TEST_ROOT_FOLDER, raising=True)
    return model


def test_has_no_default_keys(model, path):
    meta_file = model(path)
    assert not meta_file.DEFAULT_KEYS
