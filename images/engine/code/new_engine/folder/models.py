import os
import shutil

from new_engine.logger import logger


class Folder:
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name

    def create(self):
        if not self.is_present:
            logger.debug(f'Create folder “{self.path}”')
            os.makedirs(self.path)

    def delete(self):
        if self.is_present:
            logger.debug(f'Delete fodler “{self.path}”')
            shutil.rmtree(self.path)

    def rename(self, new_name):
        if self.is_present:
            old_path = self.path
            self.name = new_name
            logger.debug(f'Renaming folder “{old_path}” to “{self.path}”')
            os.rename(old_path, self.path)

    @property
    def path(self):
        return f'{self.parent}/{self.name}'

    @property
    def is_present(self):
        return os.path.isdir(self.path)
