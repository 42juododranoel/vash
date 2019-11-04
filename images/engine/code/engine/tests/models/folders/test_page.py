import pytest

from engine.tests.conftest import TEST_ROOT_FOLDER
from engine.models.folders.page import Page
from engine.models.folders.template import Template
from engine.models.files.html_file import HtmlFile


@pytest.fixture(params=[Page])
def model(request):
    return request.param


@pytest.mark.parametrize('file_name', ['meta'])
def test_get_files_has_required_files(model, path, file_name):
    page = model(path)
    assert file_name in page._get_files()


def test_get_files_returns_files_under_patched_root(model, path):
    page = model(path)
    files = page._get_files()
    for key, file in files.items():
        assert file.path.startswith(TEST_ROOT_FOLDER)


def test_render_renders_when_created(model, path):
    page = model(path)
    page.create()
    main_template = Template.get_main_template()
    main_template.create()
    HtmlFile(f'{main_template.absolute_path}/main.html').create()
    for template in page.files['meta'].templates:
        template.create()
    page.render()


def test_render_fails_when_not_created(model, path):
    page = model(path)
    pytest.raises(ValueError, page.render)


def test_meta_doesnt_mind_if_template_is_not_specified(model, path):
    page = model(path)
    page.create()
    page.files['meta'].write({'lol': 42})
    assert 'template' not in page.meta


def test_meta_returns_page_meta_merged_with_template_meta(model, path):
    page = model(path)
    page.create()
    main_template = Template.get_main_template()
    main_template.create()
    HtmlFile(f'{main_template.absolute_path}/main.html').create()
    for template in page.files['meta'].templates:
        template.create()
    page.files['meta'].templates[0].files['meta'].write({'foobar': 'baz'})
    page.files['meta'].write({'foobar': 42})
    assert page.meta['foobar'] == 42


def test_contents_return_dictionary_of_html_files(model, path):
    page = model(path)
    page.create()
    file_name = 'test'
    HtmlFile(f'{page.absolute_path}/{file_name}.html').create()
    assert file_name in page.contents.raw
    assert isinstance(page.contents.raw[file_name], HtmlFile)
