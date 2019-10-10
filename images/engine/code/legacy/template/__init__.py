import argparse
from functools import partial

from legacy.template.commands.create import (
    create,
    argument_parser as create__argument_parser,
)
from legacy.constants import _


def get_command(args):
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('command', help=_('A command to execute'))

    namespace, arguments = argument_parser.parse_known_args(args)

    if namespace.command == 'create':
        command_arguments = create__argument_parser.parse_args(arguments)
        return partial(create, **vars(command_arguments))
    else:
        raise SystemExit(_(f'Unknown command {namespace.command}'))
