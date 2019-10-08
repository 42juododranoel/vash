import click

from new_engine.commands.validators import (
    clean_path,
    clean_paths,
)
from new_engine.commands.resource import (
    create_resources,
    delete_resources,
    rename_resource,
)
from new_engine.models.page import Page


@click.command()
@click.argument('paths', nargs=-1, callback=clean_paths)
def create_pages(paths):
    create_resources(Page, paths)


@click.command()
@click.argument('paths', nargs=-1, callback=clean_paths)
def delete_pages(paths):
    delete_resources(Page, paths)


@click.command()
@click.argument('path', callback=clean_path)
@click.argument('new_path', callback=clean_path)
def rename_page(path, new_path):
    rename_resource(Page, path, new_path)


page_commands = [
    create_pages,
    delete_pages,
    rename_page,
]
