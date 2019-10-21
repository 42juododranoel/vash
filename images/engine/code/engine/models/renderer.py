import os

from engine.utilities import merge_mappings
from engine.models.files.html_file import HtmlFile
from engine.models.folders.template import Template


class Renderer:
    def __init__(self, page):
        self.page = page

    def _get_meta(self):
        page_meta = self.page.files['meta'].read()
        template_paths = page_meta['template'].split('/')
        meta = {}
        for template_path in template_paths:
            template = Template(template_path)
            template_meta = template.get_meta()
            meta = merge_mappings(meta, template_meta)
        else:
            meta.update(page_meta)
            return meta

    def _get_functions(self):
        functions = {'link': lambda *args, **kwargs: 'FOOBAR'}
        functions['picture'] = functions['link']
        return functions

    def _get_scripts(self, meta):
        return meta.get('scripts', [])

    def _get_styles(self):
        return

    def _get_contents(self):
        contents = {}
        for file_name in os.listdir(self.page.path):
            if file_name.endswith('.html'):
                file = HtmlFile(f'{self.page.path}/{file_name}')
                name = file_name.rpartition('.html')[0]
                contents[name] = file
        else:
            return contents

    def _get_blocks(self, template_names):
        blocks = {}
        for block_name in ['meta', 'body']:
            block_file = None
            for template_name in template_names:
                html_file = HtmlFile(
                    f'/resources/templates/{template_name}/{block_name}.html')
                if html_file.is_present:
                    block_file = html_file
            else:
                blocks[block_name] = block_file
        else:
            return blocks

    def _render_scripts(self, scripts):
        html = ''
        for script_data in scripts:
            script_attributes = ' '.join(
                [f'{key}="{script_data[key]}"' for key in script_data])
            html += f'<script defer="defer" {script_attributes}></script>'
        else:
            return {'scripts': html}

    def _render_styles(self):
        return

    def _render_file_mapping(self, file_mapping, context):
        return {
            name: file.render(context) if file else ''
            for name, file in file_mapping.items()
        }

    def render(self):
        meta = self._get_meta()
        functions = self._get_functions()  # This is a hack
        context = merge_mappings(meta.copy(), functions)

        scripts = self._get_scripts(meta)
        scripts_html = self._render_scripts(scripts)
        context.update(scripts_html)

        contents = self._get_contents()
        contents_html = self._render_file_mapping(contents, context)
        context.update(contents_html)

        template_names = meta['template'].split('/')
        blocks = self._get_blocks(template_names)
        blocks_html = self._render_file_mapping(blocks, context)
        context.update(blocks_html)

        # Add sanitizing

        content = HtmlFile(
            f'/resources/templates/default/default.html').render(context)
        print(content)

        # for post_processor in meta.get('post-processors', []):
        #     if post_processor == 'brotler':
        #         from engine.models.processors.brotler import Brotler
        #         Brotler.process_file(self.files['html'])
        #         Brotler.process_file(self.files['json'])
