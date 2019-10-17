from engine.utilities import merge_mappings
from engine.models.files.file import File
from legacy.page.commands.render import render as legacy_render
from engine.models.resources.resource import Resource
from engine.models.resources.template import Template
from engine.models.files.page_meta_file import PageMetaFile


class Page(Resource):
    ROOT_FOLDER = f'{Resource.ROOT_FOLDER}/pages'
    RENDERED_HTML_FOLDER = f'{ROOT_FOLDER}/_html'
    RENDERED_JSON_FOLDER = f'{ROOT_FOLDER}/_json'

    def _get_files(self):
        return {
            'meta': PageMetaFile(f'{self.path}/{self.name}.json'),
            'html': File(f'{self.RENDERED_HTML_FOLDER}/{self.name}.html'),
            'json': File(f'{self.RENDERED_JSON_FOLDER}/{self.name}.json'),
        }

    def _get_meta(self):
        page_meta = self.files['meta'].read()
        template_paths = page_meta['new_template'].split('/')
        meta = {}
        for template_path in template_paths:
            template = Template(template_path)
            template_meta = template.get_meta()
            merge_mappings(meta, template_meta)
        else:
            meta.update(page_meta)
            return meta

    def render(self):
        meta = self._get_meta()

        html_content, json_content = legacy_render(slug=self.name, page_meta=meta)

        self.files['html'].write(html_content)
        self.files['json'].write(json_content)

        for post_processor in meta.get('post-processors', []):
            if post_processor == 'brotler':
                from engine.models.processors.brotler import Brotler
                Brotler.process_file(self.files['html'])
                Brotler.process_file(self.files['json'])
