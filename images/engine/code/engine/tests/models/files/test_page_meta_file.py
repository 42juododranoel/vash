import pytest

from engine.models.files.page_meta_file import PageMetaFile


@pytest.mark.parametrize('key', ['slug', 'type', 'title'])
def test_key_in_default_keys(create, file_path, key):
    created_page_meta_file = create(PageMetaFile, file_path)
    assert key in created_page_meta_file.DEFAULT_KEYS
