import os
import shutil

from new_engine.logger import logger


class Node:
    def __init__(self, path: str):
        absolute_path = path if path.startswith('/') else self._get_absolute_path(path)
        self.parent, _, self.name = absolute_path.rpartition('/')

    @property
    def is_present(self):
        return self._check_presence(self.path)

    @property
    def path(self):
        return f'{self.parent}/{self.name}'

    def _get_absolute_path(self, path):
        return os.path.abspath(path)

    def create(self):
        if not self.is_present:
            logger.debug(f'Create “{self.path}”')
            if self.parent:  # Parent may be '' if path is 'plain', no 'hie/rar/chy'
                os.makedirs(self.parent, exist_ok=True)
            self._create(self.path)

    def delete(self):
        if self.is_present:
            logger.debug(f'Delete “{self.path}”')
            self._delete(self.path)

    def move(self, new_path):
        if self.is_present:
            logger.debug(f'Moving “{self.path}” to “{new_path}”')
            old_path = self.path
            self.__init__(new_path)
            shutil.move(old_path, self.path)
