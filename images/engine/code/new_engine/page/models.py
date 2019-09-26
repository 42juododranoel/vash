import re
import os
import shutil

from new_engine.logger import logger
from new_engine.errors import ValidationError
from new_engine.constants import PAGES_FOLDER
from new_engine.file.models import File
from new_engine.folder.models import Folder


class Page:
    def __init__(self, path: str):
        self.path = path
        self.parents, _, self.slug = self.path.rpartition('/')

        self.folder = Folder(f'{PAGES_FOLDER}/{self.path}')
        self.files = {'meta': File(self.folder, self.slug, 'json')}

    @staticmethod
    def validate_path(path):
        pattern = r'[-\w/]+'
        if not re.fullmatch(pattern, path):
            raise ValidationError(f'Invalid page path. Use pattern “{pattern}”.')

    def validate(self):
        self.validate_path(self.path)

    def create(self):
        """Create folder structure and files"""
        logger.info(f'Creating page “{self.slug}”...')
        self.folder.create()
        for _, file in self.files.items():
            file.create()

    def delete(self):
        """Delete folder structure and files"""
        logger.info(f'Deleting page “{self.slug}”...')
        self.folder.delete()

    def rename(self, new_path):
        """Change page path and rename all occurencies of this page in all files"""
        logger.info(f'Renaming page “{self.path}” to “{new_path}”...')

        self.folder.move(f'{PAGES_FOLDER}/{new_path}')

        new_slug = new_path.split('/')[-1]
        for _, file in self.files.items():
            file.rename(new_slug)

        path = self.path
        while '/' in path:
            path = path.rpartition('/')[0]
            folder = Folder(f'{PAGES_FOLDER}/{path}')
            if folder.is_empty:
                folder.delete()
