import re

import click

from new_engine.page.models import Page


def validate_path(path):
    pattern = r'[-a-zA-Z0-9/]+'
    if re.fullmatch(pattern, path):
        return path
    else:
        raise click.BadParameter(f'Invalid page path “{path}”. Use pattern “{pattern}”.')


def clean_paths(context, parameter, value):
    return [validate_path(path) for path in value]


def clean_path(context, parameter, value):
    return validate_path(value)


@click.command()
@click.argument('paths', nargs=-1, callback=clean_paths)
def create_pages(paths):
    for path in paths:
        page = Page(path)
        page.create()


@click.command()
@click.argument('paths', nargs=-1, callback=clean_paths)
def delete_pages(paths):
    for path in paths:
        page = Page(path)
        page.delete()


@click.command()
@click.argument('path', callback=clean_path)
@click.argument('new_path', callback=clean_path)
def rename_page(path, new_path):
    page = Page(path)
    page.rename(new_path)


page_commands = [
    create_pages,
    delete_pages,
    rename_page,
]
