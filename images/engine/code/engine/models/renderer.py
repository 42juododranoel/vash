import os

from jinja2 import Markup
from jinja2 import Template as JinjaTemplate

from engine.utilities import merge_mappings
from engine.models.files.json_file import JsonFile
from engine.models.files.html_file import HtmlFile
from engine.models.folders.template import Template


def get_templatetags():
    templatetags = {'link': lambda *args, **kwargs: 'FOOBAR'}
    templatetags['picture'] = templatetags['link']  # TODO: Temporary hack
    return templatetags


class Renderer:
    DEFAULT_TEMPLATE_NAMES = ['meta', 'body', 'styles', 'scripts']
    REQUIRED_TEMPLATE_NAMES = ['meta', 'body']

    DEFAULT_TEMPLATE_PATH = 'default/default.html'

    BLOCKS = {
        'styles': {
            'template': '<link {attributes}/>',
            'attributes': {'rel': 'stylesheet'},
        },
        'scripts': {
            'template': '<script {attributes}></script>',
            'attributes': {'defer': 'true'},
        }
    }

    TEMPLATETAGS = get_templatetags()

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
    def _render_block(block_name, block_tags):
        block = Renderer.BLOCKS[block_name]
        rendered_block = ''
        for block_tag in block_tags:
            block_tag.update(block['attributes'])
            attribute_pairs = [f'{key}="{value}"' for key, value in block_tag.items()]
            attributes = ' '.join(attribute_pairs)
            rendered_block += block['template'].format(attributes=attributes)
        else:
            return {block_name: rendered_block, f'raw_{block_name}': block_tags}

    @staticmethod
    def render_page(page):
        if not page.is_present:
            raise ValueError('Can\'t render missing page')

        context = Renderer.TEMPLATETAGS
        page_meta = page.files['meta'].read()

        # Combine page meta with template meta
        template_paths = page_meta['template'].split(' > ')
        templates = [Template(path) for path in template_paths]
        for template in templates:
            template_meta = template.files['meta'].read()
            context = merge_mappings(context, template_meta)
        context.update(page_meta)  # Page meta owerrides template meta

        # Render blocks `styles` and `scripts`
        for block_name in ['styles', 'scripts']:
            block_tags = page_meta.get(block_name, [])
            context.update(Renderer._render_block(block_name, block_tags))

        # Render page contents — all HTML files inside page folder
        content_files = Renderer._get_content_files(page)
        rendered_html_files = Renderer._render_html_files(content_files, context)
        context.update(rendered_html_files)

        # Render page templates hierarchy — meta `template` attribute
        template_files = Renderer._get_template_files(templates)
        rendered_template_files = Renderer._render_html_files(template_files, context)
        context.update(rendered_template_files)

        # Render page as HTML via default template
        default_template = Template(Renderer.DEFAULT_TEMPLATE_PATH)
        default_template_file = HtmlFile(default_template.absolute_path)
        rendered_html = Renderer._render_html_file(default_template_file, context)

        # Render page as JSON for Seamless API and Seamless.js
        rendered_json = {}
        for default_template_name in Renderer.DEFAULT_TEMPLATE_NAMES:
            if default_template_name in ['scripts', 'styles']:
                value = context[f'raw_{default_template_name}']  # Seamless.js uses attribute structure for simplicity
            else:
                value = context.get(default_template_name, '')
            rendered_json[default_template_name] = value

        # Write rendered contents to files
        html_file = HtmlFile(f'/resources/assets/html/{page.path}.html')
        html_file.write(rendered_html)
        json_file = JsonFile(f'/resources/assets/json/{page.path}.json')
        json_file.write(rendered_json)

        return {'html': rendered_html, 'json': rendered_json}

    def render_related_pages():
        # - список релейтедов
        # - отрендеренный джейсон
        # Для каждой релейтед
        #     В её отрендеренном джейсоне обновить кусочек с этой страницей
        pass
