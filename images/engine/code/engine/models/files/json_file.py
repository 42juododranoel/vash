from engine.models.file import File


class JsonFile(File):
    def _get_initial_content(self):
        return '{}'
