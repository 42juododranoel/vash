from shutil import copy

from django.conf import settings
from filer.models import Image, Folder
from django.core.files import File
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('file_name')
        parser.add_argument('-fi', '--file_id')
        parser.add_argument('-di', '--directory_id')

    def handle(self, **options):
        file_path = f'{settings.MEDIA_FOLDER_TEMPORARY}/{options["file_name"]}'

        if options['file_id']:
            image = Image.objects.get(id=options['file_id'])
            copy(file_path, image.path)
            image.save()

            self.stdout.write(f'Replaced {options["file_name"]} with newer image')

        else:
            folder = None
            if options['directory_id']:
                folder = Folder.objects.get(id=options['directory_id'])

            with open(file_path, 'rb') as file:
                Image.objects.create(
                    original_filename=options['file_name'],
                    file=File(file, name=options['file_name']),
                    owner=User.objects.get(username='admin'),
                    folder=folder,
                )

            self.stdout.write(
                f'Loaded {options["file_name"]}'
                f' to {folder.name}' if folder else ''
            )
