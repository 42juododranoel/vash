import json

from engine.models.files.file import File


class JsonFile(File):
    def _get_initial_content(self):
        return {}

    def _serialize(self, content):
        return json.dumps(content, indent=2)

    def _deserialize(self, content):
        return json.loads(content)
