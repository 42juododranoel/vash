import re

import click

from new_engine.template.models import Template


def validate_name(name):
    pattern = r'[\w-]+'
    if re.fullmatch(pattern, name):
        return name
    else:
        raise click.BadParameter(f'Invalid template name “{name}”. Use pattern “{pattern}”.')


def clean_names(context, parameter, value):
    return [validate_name(name) for name in value]


def clean_name(context, parameter, value):
    return validate_name(value)


@click.command()
@click.argument('names', nargs=-1, callback=clean_names)
def create_templates(names):
    for name in names:
        template = Template(name)
        template.create()


@click.command()
@click.argument('names', nargs=-1, callback=clean_names)
def delete_templates(names):
    for name in names:
        template = Template(name)
        template.delete()


@click.command()
@click.argument('name', callback=clean_name)
@click.argument('new_name', callback=clean_name)
def rename_template(name, new_name):
    template = Template(name)
    template.rename(new_name)


template_commands = [
    create_templates,
    delete_templates,
    rename_template,
]
