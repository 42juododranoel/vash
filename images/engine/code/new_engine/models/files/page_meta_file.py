from new_engine.models.files.meta_file import MetaFile


class PageMetaFile(MetaFile):
    DEFAULT_KEYS = {
        'title': '',
        'slug': '',
        'type': 'page',
    }
