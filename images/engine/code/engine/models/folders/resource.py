from engine.models.folders._.folder import Folder


class Resource(Folder):
    ROOT_FOLDER = '/resources'

    def __init__(self, path: str):
        super().__init__(path)
        self.files = self._get_files()

    def _get_files(self):
        return {}

    def create(self):
        super().create()
        for _, file in self.files.items():
            file.create()
