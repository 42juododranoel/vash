from click.testing import CliRunner

from engine.commands.page import render_page
from engine.tests.conftest import RESOURCE_PATHS
from engine.models.resources.page import Page


# def test_render_page_works(create, resource_path):
#     create(Page, resource_path)
#     cli_runner = CliRunner()
#     command_result = cli_runner.invoke(render_page, [resource_path])
#     assert command_result.exit_code == 0
#
#
# def test_render_page_accepts_multiple_paths(create):
#     for resource_path in RESOURCE_PATHS:
#         create(Page, resource_path)
#     cli_runner = CliRunner()
#     command_result = cli_runner.invoke(render_page, RESOURCE_PATHS)
#     assert command_result.exit_code == 0
