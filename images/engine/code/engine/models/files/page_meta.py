from engine.models.files.meta import MetaFile
from engine.models.folders.template import Template
from engine.utilities import merge_mappings


class PageMetaFile(MetaFile):
    DEFAULT_KEYS = {
        'title': '',
        'slug': '',
        'template': 'main',
    }

    @property
    def templates(self):
        try:
            template_paths = self['template'].split(' > ')
        except KeyError:
            return []
        else:
            return [Template(path) for path in template_paths]

    @property
    def template_meta(self):
        meta = {}
        for template in self.templates:
            template_meta = template.meta.read()
            merge_mappings(meta, template_meta)
        else:
            return meta
