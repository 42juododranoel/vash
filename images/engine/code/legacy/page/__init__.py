import os
import argparse
from functools import partial

from legacy.page.commands.render import (
    render,
    get_argument_parser as render__argument_parser_getter,
)
from legacy.constants import (
    _,
    PAGES_FOLDER
)

os.makedirs(PAGES_FOLDER, exist_ok=True)
os.makedirs(f'{PAGES_FOLDER}/_html', exist_ok=True)
os.makedirs(f'{PAGES_FOLDER}/_json', exist_ok=True)


def get_command(args):
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('command', help=_('A command to execute.'))

    namespace, arguments = argument_parser.parse_known_args(args)

    if namespace.command == 'create':
        command_arguments = create__argument_parser.parse_args(arguments)
        return partial(create, **vars(command_arguments))
    elif namespace.command == 'render':
        argument_parser = render__argument_parser_getter()
        command_arguments = argument_parser.parse_args(arguments)
        return partial(render, **vars(command_arguments))
    else:
        raise SystemError(_(f'Unknown command “{namespace.command}”.'))
