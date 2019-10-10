import click

from engine.commands.cli import cli
from engine.commands.validators import clean_path, clean_paths
from engine.models.resources.page import Page
from legacy.page.commands.create import create
from legacy.page.commands.render import render


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


@cli.command()
@click.argument('slug')
def legacy_create_page(slug):
    create(slug)


@cli.command()
@click.argument('slug')
def legacy_render_page(slug):
    render(slug)


page_commands = [
    create_page,
    delete_page,
    legacy_create_page,
    legacy_render_page,
]
