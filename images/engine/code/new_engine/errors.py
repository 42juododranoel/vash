from sys import exit
from logging import getLogger

logger = getLogger('new_manage')


def error(message):
    logger.error(message)
    exit(1)


class ValidationError(Exception):
    pass
