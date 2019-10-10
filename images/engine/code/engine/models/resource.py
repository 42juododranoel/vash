from engine.models.folder import Folder


class Resource(Folder):
    def __init__(self, path: str):
        super().__init__(path)
        self.files = self._get_files()

    @property
    def root_folder(self):
        return '/resources'

    def _get_absolute_path(self, path):
        return f'{self.root_folder}/{path}'

    def _get_files(self):
        return {}

    def create(self):
        super().create()
        for _, file in self.files.items():
            file.create()

    def move(self, new_path):
        old_path = self.path

        new_file_name = new_path.rpartition('/')[-1]
        for _, file in self.files.items():
            file_extension = file.name.rpartition('.')[-1]
            new_file_path = f'{file.parent}/{new_file_name}.{file_extension}'
            file.move(new_file_path)

        super().move(new_path)

        while '/' in old_path:
            old_path = old_path.rpartition('/')[0]
            folder = Folder(old_path)
            if folder.is_present and folder.is_empty:
                folder.delete()
