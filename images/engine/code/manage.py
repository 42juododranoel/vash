from engine.commands.cli import cli
from engine.commands.page import page_commands
from engine.commands.template import template_commands


if __name__ == '__main__':
    for commands in [page_commands, template_commands]:
        for command in commands:
            cli.add_command(command)
    else:
        cli()
