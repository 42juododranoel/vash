from engine.models.folders.bases.folder import Folder


class Resource(Folder):
    ROOT_FOLDER = '/resources'

    @property
    def files(self):
        return {}

    def create(self):
        super().create()
        for _, file in self.files.items():
            file.create()
