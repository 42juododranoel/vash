from engine.models.renderer import Renderer
from engine.models.folders.resource import Resource
from engine.models.files.page_meta_file import PageMetaFile


class Page(Resource):
    ROOT_FOLDER = f'{Resource.ROOT_FOLDER}/pages'

    def _get_files(self):
        return {'meta': PageMetaFile(f'{self.absolute_path}/{self.name}.json')}

    def render(self):
        renderer = Renderer()
        renderer.render_page(self)
