import json

from engine.models.files.bases.file import File


class JsonFile(File):
    INITIAL_KEYS = {}

    def __getitem__(self, key):
        return self.read()[key]

    def __setitem__(self, key, item):
        if not self.is_created:
            self.create()
        content = self.read()
        content[key] = item
        self.write(content)

    def _get_initial_content(self):
        return self.INITIAL_KEYS

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

    def update(self, items):
        if not self.is_created:
            self.create()
        content = self.read()
        for key in items:
            content[key] = items[key]
        else:
            self.write(content)
