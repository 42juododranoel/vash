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
from new_engine.models.template import Template


@click.command()
@click.argument('paths', nargs=-1, callback=clean_paths)
def create_templates(paths):
    create_resources(Template, paths)


@click.command()
@click.argument('paths', nargs=-1, callback=clean_paths)
def delete_templates(paths):
    delete_resources(Template, paths)


@click.command()
@click.argument('path', callback=clean_path)
@click.argument('new_path', callback=clean_path)
def rename_template(path, new_path):
    rename_resource(Template, path, new_path)


template_commands = [
    create_templates,
    delete_templates,
    rename_template,
]
