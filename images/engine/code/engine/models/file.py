import os

from engine.models.node import Node


class File(Node):
    def _create(self, path):
        with open(path, 'w') as file:
            file.write(self._get_initial_content())

    @staticmethod
    def _delete(path):
        os.remove(path)

    @staticmethod
    def _check_presence(path):
        return os.path.isfile(path)

    def _get_initial_content(self):
        return ''
