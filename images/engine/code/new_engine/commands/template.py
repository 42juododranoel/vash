import click

from new_engine.commands.cli import cli
from new_engine.models.template import Template
from new_engine.commands.validators import clean_path, clean_paths


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
