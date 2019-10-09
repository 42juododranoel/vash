import json

from new_engine.models.files.json_file import JsonFile


class MetaFile(JsonFile):
    DEFAULT_KEYS = {}

    def _get_initial_content(self):
        return json.dumps(self.DEFAULT_KEYS, indent=2)
