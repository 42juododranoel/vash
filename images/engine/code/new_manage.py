import logging
from sys import argv
from argparse import ArgumentParser

from new_engine.errors import error
from new_engine.logger import logger
from new_engine.template.commands import command_switch as template_commands


if __name__ == '__main__':
    namespace_parser = ArgumentParser()
    namespace_parser.add_argument('command')
    namespace_parser.add_argument('-v', '--verbose', help='Show more verbose output.')
    namespace, remaining_arguments = namespace_parser.parse_known_args(argv[1:])

    command_switch = {}
    command_switch.update(template_commands)

    try:
        command = command_switch[namespace.command]
    except KeyError:
        error(f'Unknown command {namespace.command}.')

    if namespace.verbose:
        logging.setLevel('DEBUG')

    command(remaining_arguments).dispatch()
