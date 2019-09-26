import os
import shutil

from new_engine.logger import logger


class Folder:
    def __init__(self, path: str):
        self.parent, _, self.name = path.rpartition('/')

    def create(self):
        if not self.is_present:
            logger.debug(f'Create folder “{self.path}”')
            os.makedirs(self.path)

    def delete(self):
        if self.is_present:
            logger.debug(f'Delete fodler “{self.path}”')
            shutil.rmtree(self.path)

    def move(self, new_path):
        if self.is_present:
            logger.debug(f'Moving folder “{self.path}” to “{new_path}”')
            old_path = self.path
            self.__init__(new_path)
            self.create()
            os.rename(old_path, new_path)

    @property
    def path(self):
        return f'{self.parent}/{self.name}'

    @property
    def is_present(self):
        return os.path.isdir(self.path)

    @property
    def is_empty(self):
        return not os.listdir(self.path)
