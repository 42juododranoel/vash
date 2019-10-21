import os

from click import echo

from engine.models.node import Node


class File(Node):
    def read(self, is_binary=False):
        if self.is_present:
            echo(f'Read from “{self.path}”')
            return self._read(is_binary=is_binary)

    def write(self, content):
        if not self.is_present:
            self.create()
        echo(f'Write to “{self.path}”')
        self._write(content)

    def _create(self, path):
        initial_content = self._get_initial_content()
        self._write(initial_content)

    def _read(self, is_binary):
        open_mode = 'rb' if is_binary else 'r'
        with open(self.absolute_path, open_mode) as file:
            return file.read()

    def _write(self, content):
        open_mode = 'wb' if isinstance(content, bytes) else 'w'
        with open(self.absolute_path, open_mode) as file:
            file.write(content)

    def _delete(self, path):
        os.remove(path)

    def _check_presence(self, path):
        return os.path.isfile(path)

    def _get_initial_content(self):
        return ''
