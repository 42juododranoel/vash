from engine.models.resources.resource import Resource
from engine.models.files.template_meta_file import TemplateMetaFile


class Template(Resource):
    ROOT_FOLDER = f'{Resource.ROOT_FOLDER}/templates'

    def _get_files(self):
        return {'meta': TemplateMetaFile(f'{self.path}/{self.name}.json')}

    def get_meta(self):
        return self.files['meta'].read()
