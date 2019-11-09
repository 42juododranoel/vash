from engine.models.files.bases.file import File


class BinaryFile(File):
    def _read(self):
        with open(self.absolute_path, 'rb') as file:
            return file.read()

    def _write(self, content):
        with open(self.absolute_path, 'wb') as file:
            file.write(content)
