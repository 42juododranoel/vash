import pytest

from engine.models.files.page_meta_file import PageMetaFile


@pytest.fixture(params=[PageMetaFile])
def model(request, capybara_patch):
    return capybara_patch(request.param)


@pytest.mark.parametrize('key', ['slug', 'type', 'title'])
def test_key_in_default_keys(model, path, key):
    page_meta_file = model(path)
    assert key in page_meta_file.DEFAULT_KEYS
