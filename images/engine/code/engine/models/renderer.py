import os

from jinja2 import Markup
from jinja2 import Template as JinjaTemplate

from engine.utilities import merge_mappings
from engine.models.files.html_file import HtmlFile
from engine.models.folders.template import Template


def get_templatetags():
    templatetags = {'link': lambda *args, **kwargs: 'FOOBAR'}
    templatetags['picture'] = templatetags['link']  # TODO: Temporary hack
    return templatetags


class Renderer:
    REQUIRED_TEMPLATE_NAMES = ['meta', 'body']

    MAIN_TEMPLATE_PATH = 'default/default.html'

    PAGES_ROOT = '/resources/pages'
    TEMPLATES_ROOT = '/resources/templates'

    templatetags = get_templatetags()

    @staticmethod
    def _get_all_meta(page_meta, templates):
        all_meta = {}
        for template in templates:
            template_meta = template.files['meta'].read()
            all_meta = merge_mappings(all_meta, template_meta)
        else:
            all_meta.update(page_meta)  # Page meta overrides template meta
            return all_meta

    @staticmethod
    def _get_content_files(page):
        content_files = {}
        for file_name in os.listdir(page.absolute_path):
            if file_name.endswith('.html'):
                name = file_name.rpartition('.html')[0]
                content_files[name] = HtmlFile(f'{page.absolute_path}/{file_name}')
        else:
            return content_files

    @staticmethod
    def _get_template_files(templates):
        template_files = {}

        for template_name in Renderer.REQUIRED_TEMPLATE_NAMES:
            latest_template_file_in_hierarchy = None

            for template in templates:
                template_file = HtmlFile(f'{template.absolute_path}/{template_name}.html')
                if template_file.is_present:
                    latest_template_file_in_hierarchy = template_file
            else:
                template_files[template_name] = latest_template_file_in_hierarchy
        else:
            return template_files

    @staticmethod
    def _render_tags(tags, tag_template):
        rendered_tags = ''
        for tag in tags:
            attributes = ' '.join([f'{key}="{tag[key]}"' for key in tag])
            rendered_tags += tag_template.format(attributes=attributes)
        else:
            return rendered_tags

    @staticmethod
    def _render_styles(styles):
        return Renderer._render_tags(styles, '<link rel="stylesheet" {attributes}/>')

    @staticmethod
    def _render_scripts(scripts):
        return Renderer._render_tags(scripts, '<script defer="defer" {attributes}></script>')

    @staticmethod
    def _render_html_file(html_file, context):
        with open(html_file.absolute_path) as file:
            jinja_file = JinjaTemplate(file.read())

        rendered_file = jinja_file.render(**context)
        unescaped_file = Markup(rendered_file)
        return unescaped_file

    @staticmethod
    def _render_html_files(html_files, context):
        return {
            name: Renderer._render_html_file(file, context) if file else ''
            for name, file in html_files.items()
        }

    @staticmethod
    def render_page(page):
        if not page.is_present:
            raise ValueError('Can\'t render missing page')

        context = {}
        page_meta = page.files['meta'].read()

        styles = page_meta.get('styles', [])
        rendered_styles = Renderer._render_styles(styles)
        context.update(styles=rendered_styles)

        scripts = page_meta.get('scripts', [])
        rendered_scripts = Renderer._render_scripts(scripts)
        context.update(scripts=rendered_scripts)

        context.update(Renderer.templatetags)
        template_paths = page_meta['template'].split(' > ')
        templates = [Template(path) for path in template_paths]
        all_meta = Renderer._get_all_meta(page_meta, templates)
        context.update(all_meta)

        content_files = Renderer._get_content_files(page)
        rendered_html_files = Renderer._render_html_files(content_files, context)
        context.update(rendered_html_files)

        template_files = Renderer._get_template_files(templates)
        rendered_template_files = Renderer._render_html_files(template_files, context)
        context.update(rendered_template_files)

        main_template = Template(Renderer.MAIN_TEMPLATE_PATH)
        main_template_file = HtmlFile(main_template.absolute_path)
        rendered_main_template_file = Renderer._render_html_file(main_template_file, context)
        print(rendered_main_template_file)

        # Sanitize, Json, post-process
