import click

from engine.commands.cli import cli
from engine.commands.validators import clean_paths
from engine.models.folders.page import Page


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


@cli.command(aliases=['render-pages'])
@click.argument('paths', nargs=-1, callback=clean_paths)
def render_page(paths):
    for path in paths:
        page = Page(path)
        page.create()
        page.render()


page_commands = [
    create_page,
    render_page,
    delete_page,
]
