import click

from engine.commands.cli import cli
from engine.commands.validators import clean_path, clean_paths
from engine.models.resources.page import Page


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
def legacy_render_page(slug):
    from engine.models.files.file import File
    from engine.models.processors.brotler import Brotler
    from legacy.page.commands.render import render

    rendered_files = render(slug)

    for rendered_file in rendered_files:
        file = File(rendered_file['path'])
        file.write(rendered_file['content'])
        Brotler.process_file(file)


page_commands = [
    create_page,
    delete_page,
    legacy_render_page,
]
