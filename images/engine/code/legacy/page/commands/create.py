import os
import argparse
from pathlib import Path

from legacy.constants import PAGES_FOLDER, SLUG_HELP_TEXT


argument_parser = argparse.ArgumentParser()
argument_parser.add_argument('-s', '--slug', help=SLUG_HELP_TEXT)


def create(slug):
    page_folder = f'{PAGES_FOLDER}/{slug}'
    try:
        os.makedirs(page_folder)
    except FileExistsError:
        raise SystemError(f'Page “{slug}” already exists.')
    else:
        Path(f'{page_folder}/meta.json' ).touch()
        Path(f'{page_folder}/related.json' ).touch()
