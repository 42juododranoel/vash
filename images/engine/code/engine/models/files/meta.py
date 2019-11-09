import json

from engine.models.files.json import JsonFile


class MetaFile(JsonFile):
    DEFAULT_KEYS = {}

    def _get_initial_content(self):
        return self.DEFAULT_KEYS
