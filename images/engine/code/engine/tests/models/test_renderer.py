import pytest

from engine.tests.conftest import ABSOLUTE_PATH_A, ABSOLUTE_PATH_B
from engine.models.renderer import Renderer
from engine.models.folders.page import Page
from engine.models.files.html_file import HtmlFile
from engine.models.folders.template import Template


def test_render_fails_when_page_is_not_created():
    # TODO: More specific error
    # TODO: Correct test message
    page = Page(ABSOLUTE_PATH_A)
    renderer = Renderer()
    pytest.raises(ValueError, renderer.render_page, page)


def test_render_scripts():
    # TODO: Unify with test_render_styles
    scripts = [
        {'src': 'https://example.com/assets/js/foobar.min.js'},
        {'src': '/assets/js/foobar.min.js', 'async': 'true'}
    ]
    rendered_scripts = Renderer._render_scripts(scripts)
    assert rendered_scripts == '<script defer="defer" src="https://example.com/assets/js/foobar.min.js"></script><script defer="defer" src="/assets/js/foobar.min.js" async="true"></script>'


def test_render_styles():
    # TODO: Multiple attributes with same name
    # TODO: No styles returns ''
    # TODO: &lt; and &gt; in input
    # TODO: Test base `render_tags`
    styles = [
        {'href': 'https://example.com/assets/css/foobar.min.css'},
        {'href': '/assets/css/foobar.min.css', 'crossorigin': 'anonymous'}
    ]
    rendered_styles = Renderer._render_styles(styles)
    assert rendered_styles == '<link rel="stylesheet" href="https://example.com/assets/css/foobar.min.css"/><link rel="stylesheet" href="/assets/css/foobar.min.css" crossorigin="anonymous"/>'


def test_get_all_meta():  # TODO: That needs refactoring
    # TODO: multiple templates
    # TODO: simpler page creation
    # TODO: relative paths
    # TODO: validate separators
    page = Page(ABSOLUTE_PATH_A)
    page.create()
    page_meta = page.files['meta'].read()
    page_meta['template'] = ABSOLUTE_PATH_B
    page.files['meta'].write(page_meta)

    template = Template(ABSOLUTE_PATH_B)
    template.create()
    template_meta = template.files['meta'].read()
    test_key = 'foo'
    template_meta[test_key] = 'bar'
    template.files['meta'].write(template_meta)

    template_paths = page_meta['template'].split(' > ')
    templates = [Template(path) for path in template_paths]

    all_meta = Renderer._get_all_meta(page_meta, templates)
    assert test_key in all_meta


def test_get_content_files():
    # TODO: Returns instances of HtmlFile
    page = Page(ABSOLUTE_PATH_A)
    page.create()

    HtmlFile(f'{page.absolute_path}/test.html').create()
    assert 'test' in Renderer._get_content_files(page)
