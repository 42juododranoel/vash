import pytest

from engine.models.folders.template import Template
from engine.models.files.page_meta import PageMetaFile


@pytest.fixture(params=[PageMetaFile])
def model(request):
    return request.param


@pytest.mark.parametrize('key', PageMetaFile.DEFAULT_KEYS)
def test_key_in_default_keys(model, path, key):
    page_meta_file = model(path)
    page_meta_file.create()
    assert page_meta_file.read() == page_meta_file.DEFAULT_KEYS


def test_templates_returns_list_of_templates(model, path):
    page_meta_file = model(path)
    page_meta_file.create()
    assert isinstance(page_meta_file.templates, list)
    assert isinstance(page_meta_file.templates[0], Template)


def test_template_meta_returns_merged_meta(model, path):
    page_meta_file = model(path)
    page_meta_file.create()

    page_meta_file['template'] = 'main > article'

    page_meta_file.templates[0].meta.write({'foo': {'bar': 'baz'}})
    page_meta_file.templates[1].meta.write({'foo': {'bar': 42}})

    assert page_meta_file.template_meta['foo']['bar'] == 42
