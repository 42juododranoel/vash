from new_engine.models.folder import Folder
from new_engine.models.resource import Resource
from new_engine.models.files.page_meta_file import PageMetaFile


class Page(Resource):
    @property
    def root_folder(self):
        return '/resources/pages'

    def _get_files(self):
        return {
            'meta': PageMetaFile(f'{self.path}/{self.name}.json'),
        }
