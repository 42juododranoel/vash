import os
from functools import partial

from engine.utilities import path_to_link
from engine.models.tags import TAGS
from engine.models.processors import PROCESSORS
from engine.models.files.html import HtmlFile
from engine.models.files.json import JsonFile
from engine.models.files.page_meta import PageMetaFile
from engine.models.folders.bases.resource import Resource
from engine.models.folders.template import Template


class PageContents:
    def __init__(self, page):
        self.page = page

    @property
    def raw(self):
        contents = {}
        for file_name in os.listdir(self.page.absolute_path):
            file_path = f'{self.page.absolute_path}/{file_name}'
            if os.path.isfile(file_path) and file_name.endswith('.html'):
                name = file_name.rpartition('.html')[0]
                contents[name] = HtmlFile(f'{self.page.absolute_path}/{file_name}')
        else:
            return contents

    def render(self, context):
        contents = self.raw
        for name, file in contents.items():
            contents[name] = contents[name].render(context)
        else:
            return contents


class PageBlocks:
    def __init__(self, page):
        self.page = page

    @property
    def raw(self):
        return {
            'meta': self.meta,
            'body': self.body,
            'styles': self.styles,
            'scripts': self.scripts,
        }

    def render(self, context):
        blocks = self.raw
        for name in ['meta', 'body']:
            blocks[name] = blocks[name].render(context) if blocks[name] else ''
        else:
            return blocks

    @property
    def meta(self):
        return self._get_file_block('meta')

    @property
    def body(self):
        return self._get_file_block('body')

    @property
    def styles(self):
        return self._get_tag_block('styles', {'rel': 'stylesheet'})

    @property
    def scripts(self):
        return self._get_tag_block('scripts', {'defer': 'true'})

    def _get_tag_block(self, name, attributes):
        tags = self.page.meta.get(name, [])
        for tag in tags:
            tag.update(attributes)
        return tags

    def _get_file_block(self, name):
        file = None
        latest_template_file_in_hierarchy = None
        for template in self.page.files['meta'].templates:
            template_file = HtmlFile(f'{template.absolute_path}/{name}.html')
            if template_file.is_present:
                latest_template_file_in_hierarchy = template_file
        else:
            if latest_template_file_in_hierarchy:
                file_path = latest_template_file_in_hierarchy.absolute_path
                file = HtmlFile(file_path)

        return file


class Page(Resource):
    ROOT_FOLDER = f'{Resource.ROOT_FOLDER}/pages'

    def __init__(self, path: str):
        super().__init__(path)
        self.blocks = PageBlocks(self)
        self.contents = PageContents(self)

    @property
    def link(self):
        return path_to_link(self.path)

    @property
    def meta(self):
        template_meta = self.files['meta'].template_meta
        page_meta = self.files['meta'].read()
        template_meta.update(page_meta)
        return template_meta

    def render(self):
        if not self.is_present:
            raise ValueError('Can\'t render missing page')

        context = self._get_context()
        context.update(self.meta)

        contents = self.contents.render(context)
        context.update(contents)

        blocks = self.blocks.render(context)
        context.update(blocks)

        self._render_as_html(context)
        self._render_as_json(blocks)

        self._update_relations_from_me(context['relations-from-me'])

    def _get_context(self):
        context = {
            'relations-from-me': [],
            'relations-to-me': [],
        }
        for name, tag in TAGS.items():
            context[name] = partial(tag, context=context)
        else:
            return context

    def _get_processors(self, stage, name, default):
        try:
            processors = self.meta['processors'][stage][name]
        except KeyError:
            processors = default
        finally:
            return processors

    def _get_files(self):
        return {
            'meta': PageMetaFile(f'{self.absolute_path}/{self.name}.json'),
            'html': HtmlFile(f'{Resource.ROOT_FOLDER}/assets/html/{self.path}.html'),
            'json': JsonFile(f'{Resource.ROOT_FOLDER}/assets/json/{self.path}.json'),
        }

    def _render_as_html(self, context):
        main_template = Template.get_main_template()
        html_file = HtmlFile(f'{main_template.absolute_path}/main.html')
        html = html_file.render(context)

        pre_processors = self._get_processors('pre', 'html', [])
        for name in pre_processors:
            processor = PROCESSORS[name]
            html = processor.process_content(html)

        file = self.files['html']
        file.write(html)

        post_processors = self._get_processors('post', 'html', [])
        for name in post_processors:
            processor = PROCESSORS[name]
            processor.process_file(file)

    def _render_as_json(self, blocks):
        pre_processors_by_block = self._get_processors('pre', 'json', {})
        for block_name, processors in pre_processors_by_block.items():
            for processor_name in processors:
                block = blocks[block_name]
                processor = PROCESSORS[processor_name]
                blocks[block_name] = processor.process_content(block)

        json = {
            self.link: {
                'title': self.meta['title'],
                'blocks': blocks,
            }
        }

        file = self.files['json']
        file.write(json)

        post_processors = self._get_processors('post', 'json', [])
        for name in post_processors:
            processor = PROCESSORS[name]
            processor.process_file(file)

    def _update_relations_from_me(self, relations):
        relations_from_me = {}

        for path in relations:
            related_page = Page(path)
            related_page_json = related_page.files['json'].read()
            relations_from_me[related_page.link] = related_page_json[related_page.link]
