import logging

import click

from new_engine.commands.page import page_commands
from new_engine.commands.template import template_commands


@click.group()
def command_line_interpreter():
    pass


if __name__ == '__main__':
    for commands in [page_commands, template_commands]:
        for command in commands:
            command_line_interpreter.add_command(command)
    else:
        command_line_interpreter()
