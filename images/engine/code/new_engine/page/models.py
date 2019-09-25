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

        self.folder = Folder(f'{PAGES_FOLDER}/{self.parents}', self.slug)
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
