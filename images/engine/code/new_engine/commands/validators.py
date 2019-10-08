import re

import click


def validate_path(path):
    pattern = r'[-a-zA-Z0-9/]+'
    if re.fullmatch(pattern, path):
        return path
    else:
        raise click.BadParameter(f'Invalid path “{path}”. Use pattern “{pattern}”.')


def clean_path(context, parameter, value):
    return validate_path(value)


def clean_paths(context, parameter, value):
    return [validate_path(path) for path in value]
