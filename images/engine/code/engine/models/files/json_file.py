import json

from engine.models.files.file import File


class JsonFile(File):
    def _get_initial_content(self):
        return '{}'

    def read(self, is_binary=False):
        content = super().read(is_binary=is_binary)
        return json.loads(content)
