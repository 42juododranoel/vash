from new_engine.models.resource import Resource
from new_engine.models.file import File
from new_engine.models.folder import Folder


class Page(Resource):
    @property
    def root_folder(self):
        return '/resources/pages'

    def _get_files(self):
        return {
            'meta': File(f'{self.path}/{self.name}.json'),
        }
