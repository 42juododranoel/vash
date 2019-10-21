import click

from engine.commands.cli import cli
from engine.commands.validators import clean_path, clean_paths
from engine.models.folders.template import Template


@cli.command(aliases=['create-templates'])
@click.argument('paths', nargs=-1, callback=clean_paths)
def create_template(paths):
    for path in paths:
        template = Template(path)
        template.create()


@cli.command(aliases=['delete-templates'])
@click.argument('paths', nargs=-1, callback=clean_paths)
def delete_template(paths):
    for path in paths:
        template = Template(path)
        template.delete()


template_commands = [
    create_template,
    delete_template,
]
