import re
import os
import shutil

from new_engine.logger import logger
from new_engine.errors import ValidationError
from new_engine.constants import TEMPLATES_FOLDER
from new_engine.file.models import File
from new_engine.folder.models import Folder


class Template:
    def __init__(self, name: str):
        self.name = name
        self.folder = Folder(TEMPLATES_FOLDER, self.name)
        self.files = {
            'meta': File(self.folder, self.name, 'json'),
            'template': File(self.folder, self.name, 'html'),
        }

    @staticmethod
    def validate_name(name):
        pattern = r'[\w-]+'
        if not re.fullmatch(pattern, name):
            raise ValidationError(f'Invalid template name. Use pattern “{pattern}”')

    def validate(self):
        self.validate_name(self.name)

    def create(self):
        """Create folder structure and files"""
        logger.info(f'Creating template “{self.name}”...')
        self.folder.create()
        for _, file in self.files.items():
            file.create()

    def delete(self):
        """Delete folder structure and files"""
        logger.info(f'Deleting template “{self.name}”...')
        self.folder.delete()

    def rename(self, new_name):
        """Change all occurencies of this template name in all files"""
        logger.info(f'Renaming template “{self.name}” to “{new_name}”...')

        self.folder.rename(new_name)
        for _, file in self.files.items():
            file.rename(new_name)
