import click

from new_engine.commands.cli import cli
from new_engine.commands.validators import clean_path, clean_paths
from new_engine.models.resources.page import Page


@cli.command(aliases=['create-pages'])
@click.argument('paths', nargs=-1, callback=clean_paths)
def create_page(paths):
    for path in paths:
        page = Page(path)
        page.create()


@cli.command(aliases=['delete-pages'])
@click.argument('paths', nargs=-1, callback=clean_paths)
def delete_page(paths):
    for path in paths:
        page = Page(path)
        page.delete()


page_commands = [
    create_page,
    delete_page,
]
