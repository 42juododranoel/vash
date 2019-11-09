import json

from engine.models.files.file import File


class JsonFile(File):
    def __getitem__(self, key):
        return self.read()[key]

    def __setitem__(self, key, item):
        if not self.is_present:
            self.create()
        content = self.read()
        content[key] = item
        self.write(content)

    def _get_initial_content(self):
        return {}

    def _serialize(self, content):
        return json.dumps(content, indent=2)

    def _deserialize(self, content):
        return json.loads(content)

    def get(self, key, default=None):
        try:
            value = self[key]
        except KeyError:
            value = default
        finally:
            return value
