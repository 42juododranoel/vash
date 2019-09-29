import logging

import click

from new_engine.page.commands import page_commands
from new_engine.template.commands import template_commands


@click.group()
@click.option('--verbose', is_flag=True, help="Will print verbose messages.")
def cli(verbose):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    for commands in [template_commands, page_commands]:
        for command in commands:
            cli.add_command(command)
    else:
        cli()
