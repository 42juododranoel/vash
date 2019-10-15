from engine.models.files.file import File
from engine.models.folder import Folder
from engine.models.resource import Resource


class Template(Resource):
    @property
    def root_folder(self):
        return '/resources/templates'

    def _get_files(self):
        return {
            'meta': File(f'{self.path}/{self.name}.json'),
        }
