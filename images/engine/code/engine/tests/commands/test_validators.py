import click
import pytest

from engine.commands.validators import (
    clean_path,
    clean_paths,
    validate_path,
)

GOOD_PATHS = ['foobar', 'foobar/foobar', 'foo-bar/foo-bar-123']
BAD_PATHS = ['foo_bar', 'foo-bar/foo-bar-123@']


@pytest.mark.parametrize('path', GOOD_PATHS)
def test_validate_path_ok(path):
    assert validate_path(path)


@pytest.mark.parametrize('path', BAD_PATHS)
def test_validate_path_error(path):
    pytest.raises(click.exceptions.BadParameter, validate_path, path)


@pytest.mark.parametrize('path', GOOD_PATHS)
def test_clean_path_ok(path):
    clean_path(None, None, path)


@pytest.mark.parametrize('path', BAD_PATHS)
def test_clean_path_error(path):
    pytest.raises(click.exceptions.BadParameter, clean_path, None, None, path)


def test_clean_paths_ok():
    clean_paths(None, None, GOOD_PATHS)


def test_clean_paths_error():
    pytest.raises(click.exceptions.BadParameter, clean_paths, None, None, BAD_PATHS)
