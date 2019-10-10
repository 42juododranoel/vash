import os
import gettext
import argparse
from pathlib import Path

_ = gettext.gettext

TEMPLATES_FOLDER = '/resources/templates'
os.makedirs(TEMPLATES_FOLDER, exist_ok=True)

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument('-n', '--name', help=_('0-9, a-z, A-Z, -, _..'))


def create(name):
    template_file = f'{TEMPLATES_FOLDER}/{name}.html'

    if os.path.isfile(template_file):
        raise SystemError(f'Template “{name}” already exists.')
    else:
        Path(template_file).touch()
