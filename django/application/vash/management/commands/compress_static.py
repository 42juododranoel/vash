# -*- coding: utf-8 -*-

import os
from subprocess import check_call

from brotli import compress, MODE_GENERIC
from django.conf import settings
from django.core.management.base import BaseCommand

COMPRESSIBLE_FILE_EXTENSIONS = [
    'html', 'css', 'js', 'json',
    'svg', 'txt', 'md', 'map', 'otf',
]


def get_all_files(directory):
    files = []
    for file_or_directory in os.listdir(directory):
        full_path = directory + '/' + file_or_directory
        if os.path.isdir(full_path):
            files += get_all_files(full_path)
        else:
            files.append(full_path)
    return files


def filter_compressible_files(files):
    return [
        file for file in files
        if file.rpartition('.')[2] in COMPRESSIBLE_FILE_EXTENSIONS
    ]


def compress_file(path):
    path_compressed = path + '.br'
    with open(path_compressed, 'wb') as file_compressed:
        with open(path, 'rb') as file:
            compressed_content = compress(
                file.read(),
                mode=MODE_GENERIC,
                quality=11,
                lgwin=22,
                lgblock=0,
            )
        file_compressed.write(compressed_content)
    return path_compressed


class Command(BaseCommand):
    def handle(self, **options):
        files_all = get_all_files(settings.STATIC_ROOT)
        files_filtered = filter_compressible_files(files_all)
        # steps_total = len(files_filtered)
        files_compressed = []
        for step, file in enumerate(files_filtered):
            # self.stdout.write(f'{step}/{steps_total} Compressing file "{file}"')
            files_compressed.append(compress_file(file))

        # Set same modified time for .br and original files
        check_call(['touch', *(files_filtered + files_compressed)])

        self.stdout.write(f'Compressed {len(files_filtered)} files')
