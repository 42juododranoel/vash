import os

from new_engine.logger import logger
from new_engine.folder.models import Folder


class File:
    def __init__(self, folder, name, extension):
        self.name = name
        self.folder = folder
        self.extension = extension

    def get_initial_content(self):
        return ''

    def create(self):
        if not self.is_present:
            logger.debug(f'Create file “{self.path}”')
            with open(self.path, 'w') as file:
                file.write(self.get_initial_content())

    def delete(self):
        if self.is_present:
            logger.debug(f'Delete file “{self.path}”')
            os.remove(self.path)

    def rename(self, new_name):
        if self.is_present:
            old_path = self.path
            self.name = new_name
            logger.debug(f'Renaming file “{old_path}” to “{self.path}”')
            os.rename(old_path, self.path)

    @property
    def path(self):
        return f'{self.folder.path}/{self.name}.{self.extension}'

    @property
    def is_present(self):
        return os.path.isfile(self.path)


class JsonFile(File):
    def get_initial_content(self):
        return '{}'
