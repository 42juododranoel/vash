import os

from jinja2 import Markup
from jinja2 import Template as JinjaTemplate

from engine.utilities import merge_mappings
from engine.models.files.json_file import JsonFile
from engine.models.files.html_file import HtmlFile
from engine.models.folders.template import Template


class Renderer:
    RENDERED_HTML_FOLDER_PATH = f'/resources/assets/html'
    RENDERED_JSON_FOLDER_PATH = f'/resources/assets/json'

    MAIN_TEMPLATE_PATH = '/resources/templates/default/default.html'

    BLOCK_ATTRIBUTES = {
        'styles': {'rel': 'stylesheet'},
        'scripts': {'defer': 'true'},
    }

    @staticmethod
    def jinja_render(file_path, context):
        with open(file_path) as file:
            file_content = file.read()
            jinja_file = JinjaTemplate(file_content)
        rendered_html = jinja_file.render(**context)
        unescaped_html = Markup(rendered_html)
        return unescaped_html

    @staticmethod
    def _get_templatetags():
        templatetags = {'link': lambda *args, **kwargs: 'FOOBAR'}
        templatetags['picture'] = templatetags['link']  # TODO: Temporary hack
        return templatetags

    def _get_page_meta(self, page):
        return page.files['meta'].read()

    def _get_templates(self, page_meta):
        template_paths = page_meta['template'].split(' > ')
        templates = [Template(path) for path in template_paths]
        return templates

    def _get_template_meta(self, page, templates):
        meta = {}
        for template in templates:
            template_meta = template.files['meta'].read()
            merge_mappings(meta, template_meta)
        else:
            return meta

    def _get_styles_and_scripts_blocks(self, meta):
        blocks = {}

        for block_name in ['styles', 'scripts']:
            block_tags = meta.get(block_name, [])

            for block_tag in block_tags:
                block_tag.update(self.BLOCK_ATTRIBUTES[block_name])
            else:
                blocks[block_name] = block_tags

        return blocks

    def _get_meta_and_body_blocks(self, templates, context):
        blocks = {}

        for block_name in ['meta', 'body']:
            blocks[block_name] = ''
            latest_template_file_in_hierarchy = None

            for template in templates:
                template_file = HtmlFile(f'{template.absolute_path}/{block_name}.html')
                if template_file.is_present:
                    latest_template_file_in_hierarchy = template_file

            else:
                if latest_template_file_in_hierarchy:
                    file_path = latest_template_file_in_hierarchy.absolute_path
                    blocks[block_name] = self.jinja_render(file_path, context)
        else:
            return blocks

    def _get_contents(self, page_folder_path, context):
        contents = {}
        for file_name in os.listdir(page_folder_path):
            if file_name.endswith('.html'):
                name = file_name.rpartition('.html')[0]
                file_path = f'{page_folder_path}/{file_name}'
                contents[name] = self.jinja_render(file_path, context)
        else:
            return contents

    def render_page(self, page):
        if not page.is_present:
            raise ValueError('Can\'t render missing page')

        context = self._get_templatetags()

        # Combine page meta and template meta
        meta = {}
        page_meta = self._get_page_meta(page)
        templates = self._get_templates(page_meta)
        template_meta = self._get_template_meta(page, templates)
        meta.update(template_meta)
        meta.update(page_meta)  # Page meta overrides template meta
        context.update(meta)

        # Contents are HTML files inside page folder
        contents = self._get_contents(page.absolute_path, context)
        context.update(contents)

        # Blocks are used to render main template and seamless cache
        blocks = {}
        styles_and_scripts = self._get_styles_and_scripts_blocks(meta)
        blocks.update(styles_and_scripts)
        meta_and_body = self._get_meta_and_body_blocks(templates, context)
        blocks.update(meta_and_body)
        context.update(blocks)

        # Render and save as HTML and JSON
        html_file = self._render_as_html(page, context)
        json_file = self._render_as_json(page, blocks)

        return {'html': html_file, 'json': json_file}

    def _render_as_html(self, page, context):
        html = self.jinja_render(self.MAIN_TEMPLATE_PATH, context)
        html_file_path = f'{self.RENDERED_HTML_FOLDER_PATH}/{page.path}.html'
        html_file = HtmlFile(html_file_path)
        html_file.write(html)
        return html_file

    def _render_as_json(self, page, blocks):
        json_file_path = f'{self.RENDERED_JSON_FOLDER_PATH}/{page.path}.json'
        json_file = JsonFile(json_file_path)
        json_file.write(blocks)
        return json_file
