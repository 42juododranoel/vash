import os
from functools import partial

from click import echo

from engine.utilities import merge_metas, path_to_link
from engine.models.tags import TAGS
from engine.models.processors import PROCESSORS
from engine.models.files.html import HtmlFile
from engine.models.files.json import JsonFile
from engine.models.files.page_meta import PageMetaFile
from engine.models.files.page_cache import PageCacheFile
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
            'meta': self._get_file_block('meta'),
            'body': self._get_file_block('body'),
            'styles': self._get_tag_block('styles'),
            'scripts': self._get_tag_block('scripts'),
        }

    def render(self, context):
        blocks = self.raw
        for name in ['meta', 'body']:
            blocks[name] = blocks[name].render(context) if blocks[name] else ''
        else:
            return blocks

    def _get_tag_block(self, name):
        tags = self.page.meta.get(name, [])
        for tag in tags:
            if name == 'scripts':
                tag.update({'defer': 'true'})
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


class PageRelations:
    def __init__(self, page):
        self.page = page
        self.forward = PageForwardRelations(page)
        self.backward = PageBackwardRelations(page)


class PageForwardRelations:
    def __init__(self, page):
        self.page = page

    @property
    def pages(self):
        paths = self.page.files['cache']['forward-relations']
        return [Page(path) for path in paths]

    def update(self):
        echo(f'Update “{self.page.path}” forward relations')
        relations = {}
        for page in self.pages:
            echo(f'  “{page.path}”')

            if page.files['json'].is_present:
                page_json = page.files['json'].read()
                if page.link in page_json:
                    relations[page.link] = page_json[page.link]

            if page.files['cache'].is_present:
                page_cache = page.files['cache'].read()
                relations_set = set(page_cache['backward-relations'])
                relations_set.add(self.page.path)
                relations_list = list(relations_set)
                page_cache['backward-relations'] = relations_list
                page.files['cache'].update(page_cache)

        self.page.files['json'].update(relations)


class PageBackwardRelations:
    def __init__(self, page):
        self.page = page

    @property
    def pages(self):
        paths = self.page.files['cache']['backward-relations']
        return [Page(path) for path in paths]

    def update(self):
        echo(f'Update “{self.page.path}” backward relations')
        my_json = self.page.files['json'].read()
        for page in self.pages:
            echo(f'  “{page.path}”')
            page_json = page.files['json'].read()
            page_json[self.page.link] = my_json[self.page.link]
            page.files['json'].write(page_json)


class PageRenderers:
    def __init__(self, page):
        self.page = page
        self.html = PageHtmlRenderer(self, page)
        self.json = PageJsonRenderer(self, page)

    def _get_context(self):
        context = {
            'forward-relations': [],
            'backward-relations': [],
            'page': self.page,
        }
        for name, tag in TAGS.items():
            context[name] = partial(tag, context=context)
        else:
            return context

    def _get_processors(self, stage, name, default):
        try:
            processors = self.page.meta['processors'][stage][name]
        except KeyError:
            processors = default
        finally:
            return processors

    def render(self):
        echo(f'Render “{self.page.path}”')

        if not self.page.is_present:
            raise ValueError('Can\'t render missing page')

        context = self._get_context()
        context.update(self.page.meta)

        contents = self.page.contents.render(context)
        context.update(contents)

        blocks = self.page.blocks.render(context)
        context.update(blocks)

        self.html.render(context)
        self.json.render(blocks)

        related_page_paths = context['forward-relations']
        self.page.files['cache']['forward-relations'] = related_page_paths
        self.page.relations.forward.update()

        self.page.relations.backward.update()


class PageHtmlRenderer:
    def __init__(self, renderers, page):
        self.renderers = renderers
        self.page = page

    def render(self, context):
        echo(f'Render “{self.page.path}” as HTML')

        main_template = Template.get_main_template()
        html_file = HtmlFile(f'{main_template.absolute_path}/main.html')
        html = html_file.render(context)

        pre_processors = self.renderers._get_processors('pre', 'html', [])
        for name in pre_processors:
            processor = PROCESSORS[name]
            html = processor.process_content(html)

        file = self.page.files['html']
        file.write(html)

        post_processors = self.renderers._get_processors('post', 'html', [])
        for name in post_processors:
            processor = PROCESSORS[name]
            processor.process_file(file)


class PageJsonRenderer:
    def __init__(self, renderers, page):
        self.renderers = renderers
        self.page = page

    def render(self, blocks):
        echo(f'Render “{self.page.path}” as JSON')

        pre_processors_by_block = self.renderers._get_processors('pre', 'json', {})
        for block_name, processors in pre_processors_by_block.items():
            for processor_name in processors:
                block = blocks[block_name]
                processor = PROCESSORS[processor_name]
                blocks[block_name] = processor.process_content(block)

        json = {
            self.page.link: {
                'title': self.page.meta['title'],
                'blocks': blocks,
            }
        }

        file = self.page.files['json']
        file.write(json)

        post_processors = self.renderers._get_processors('post', 'json', [])
        for name in post_processors:
            processor = PROCESSORS[name]
            processor.process_file(file)


class Page(Resource):
    ROOT_FOLDER = f'{Resource.ROOT_FOLDER}/pages'

    def __init__(self, path: str):
        super().__init__(path)
        self.blocks = PageBlocks(self)
        self.contents = PageContents(self)
        self.relations = PageRelations(self)
        self.renderers = PageRenderers(self)

    @property
    def link(self):
        return path_to_link(self.path)

    @property
    def meta(self):
        template_meta = self.files['meta'].template_meta
        page_meta = self.files['meta'].read()
        merge_metas(template_meta, page_meta)
        return template_meta

    def render(self):
        self.renderers.render()

    def _get_files(self):
        return {
            'json': JsonFile(f'{Resource.ROOT_FOLDER}/assets/json/{self.path}.json'),
            'html': HtmlFile(f'{Resource.ROOT_FOLDER}/assets/html/{self.path}.html'),
            'meta': PageMetaFile(f'{self.absolute_path}/{self.name}.json'),
            'cache': PageCacheFile(f'{self.absolute_path}/cache.json'),
        }
