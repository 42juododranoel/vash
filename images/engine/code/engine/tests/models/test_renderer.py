import pytest

from engine.tests.conftest import ABSOLUTE_PATH_A, ABSOLUTE_PATH_B
from engine.models.renderer import Renderer
from engine.models.folders.page import Page
from engine.models.files.html_file import HtmlFile
from engine.models.folders.template import Template


def test_jinja_renders_templates():
    ...


def test_jinja_renders_as_unescaped_html():
    ...


def test_get_templatetags():
    ...


def test_get_page_meta_reads_page_meta():
    ...


def test_get_templates_parses_template_hierarchy():
    ...


def test_get_template_meta_overrides_correctly():
    ...


def test_get_styles_and_scripts_blocks():
    ...


def test_get_meta_and_body_blocks():
    ...


def test_get_contents():
    ...


def test_render_as_html():
    ...


def test_render_as_json():
    ...


def test_render_page_fails_when_page_is_not_created():
    ...


def test_render_page():
    ...
