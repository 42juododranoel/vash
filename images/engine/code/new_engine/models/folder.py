import os
import shutil

from new_engine.models.node import Node


class Folder(Node):
    @staticmethod
    def _create(path):
        os.makedirs(path)

    @staticmethod
    def _delete(path):
        shutil.rmtree(path)

    @staticmethod
    def _check_presence(path):
        return os.path.isdir(path)

    @property
    def is_empty(self):
        return not os.listdir(self.path)
