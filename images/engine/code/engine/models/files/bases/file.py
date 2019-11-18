import os

from engine.models.node import Node


class File(Node):
    def read(self):
        if self.is_created:
            serialized_content = self._read()
            return self._deserialize(serialized_content)
        else:
            raise FileNotFoundError('Can\'t read from missing file.')

    def write(self, content):
        if not self.is_created:
            self.create()
        serialized_content = self._serialize(content)
        self._write(serialized_content)

    def _serialize(self, content):
        return content

    def _deserialize(self, content):
        return content

    def _create(self, path):
        initial_content = self._get_initial_content()
        serialized_content = self._serialize(initial_content)
        self._write(serialized_content)

    def _read(self):
        with open(self.absolute_path, 'r') as file:
            return file.read()

    def _write(self, content):
        with open(self.absolute_path, 'w') as file:
            file.write(content)

    def _delete(self, path):
        os.remove(path)

    def _check_presence(self, path):
        return os.path.isfile(path)

    def _get_initial_content(self):
        return ''
