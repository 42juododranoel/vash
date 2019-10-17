import pytest
from click.testing import CliRunner

from engine.tests.conftest import RESOURCE_PATHS
from engine.commands.page import create_page, delete_page
from engine.commands.template import create_template, delete_template


@pytest.mark.parametrize('command', [create_page, create_template])
def test_common_create_commands(command):
    cli_runner = CliRunner()
    command_result = cli_runner.invoke(command, RESOURCE_PATHS)
    assert command_result.exit_code == 0


@pytest.mark.parametrize('command', [delete_page, delete_template])
def test_common_delete_commands(command):
    cli_runner = CliRunner()
    command_result = cli_runner.invoke(command, RESOURCE_PATHS)
    assert command_result.exit_code == 0
