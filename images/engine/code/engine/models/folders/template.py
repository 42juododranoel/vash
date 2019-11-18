from engine.models.folders.bases.resource import Resource
from engine.models.files.template_meta import TemplateMetaFile


class Template(Resource):
    ROOT = f'{Resource.ROOT}/templates'

    @classmethod
    def get_main_template(cls):
        return cls('main')

    @property
    def meta(self):
        return self.files['meta']

    @property
    def files(self):
        return {'meta': TemplateMetaFile(f'{self.absolute_path}/_/{self.name}.json')}
