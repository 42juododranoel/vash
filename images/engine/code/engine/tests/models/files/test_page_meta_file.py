import pytest

from engine.models.files.page_meta_file import PageMetaFile
from engine.tests.conftest import TEST_ROOT_FOLDER


@pytest.fixture
def model(request, monkeypatch):
    model = PageMetaFile
    monkeypatch.setattr(model, 'ROOT_FOLDER', TEST_ROOT_FOLDER, raising=True)
    return model


@pytest.mark.parametrize('key', ['slug', 'type', 'title'])
def test_key_in_default_keys(model, path, key):
    page_meta_file = model(path)
    assert key in page_meta_file.DEFAULT_KEYS
