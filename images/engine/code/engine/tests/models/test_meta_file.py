def test_has_no_default_keys(created_meta_file):
    assert not created_meta_file.DEFAULT_KEYS


def test_title_in_default_keys(page_meta_file):
    assert 'title' in page_meta_file.DEFAULT_KEYS


def test_slug_in_default_keys(page_meta_file):
    assert 'slug' in page_meta_file.DEFAULT_KEYS


def test_type_in_default_keys(page_meta_file):
    assert 'type' in page_meta_file.DEFAULT_KEYS


def test_default_keys(template_meta_file):
    pass
