from engine.models.folders.bases.resource import Resource
from engine.models.files.template_meta import TemplateMetaFile


class Template(Resource):
    ROOT_FOLDER = f'{Resource.ROOT_FOLDER}/templates'

    @classmethod
    def get_main_template(cls):
        return cls('main')

    @property
    def meta(self):
        return self.files['meta']

    def _get_files(self):
        return {'meta': TemplateMetaFile(f'{self.absolute_path}/_/{self.name}.json')}
