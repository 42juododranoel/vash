class TestMetaFile:
    def test_has_no_default_keys(self, created_meta_file):
        assert not created_meta_file.DEFAULT_KEYS


class TestPageMetaFile:
    def test_title_in_default_keys(self, page_meta_file):
        assert 'title' in page_meta_file.DEFAULT_KEYS

    def test_slug_in_default_keys(self, page_meta_file):
        assert 'slug' in page_meta_file.DEFAULT_KEYS

    def test_type_in_default_keys(self, page_meta_file):
        assert 'type' in page_meta_file.DEFAULT_KEYS


class TestTemplateMetaFile:
    def test_default_keys(self, template_meta_file):
        pass
