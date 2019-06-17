from django.conf import settings
from filer.models import Image
from django.core.files import File
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('file_name')

    def handle(self, **options):
        file_path = f'{settings.MEDIA_FOLDER_TEMPORARY}/{options["file_name"]}'

        with open(file_path, 'rb') as file:
            Image.objects.create(
                original_filename=options['file_name'],
                file=File(file, name=options['file_name']),
                owner=User.objects.get(username='admin'),
            )

        self.stdout.write(f'Loaded {file_name}')
