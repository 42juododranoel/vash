# import pytest
# from click.testing import CliRunner
#
# from engine.commands.page import create_page, delete_page
# from engine.commands.template import create_template, delete_template
# from engine.models.folders.page import Page
# from engine.models.folders.template import Template
# from engine.tests.conftest import (
#     TEST_ROOT_FOLDER,
#     RELATIVE_PATH_A,
# )
#
#
# @pytest.fixture(params=[Page, Template])
# def model(request, monkeypatch):
#     model = request.param
#     monkeypatch.setattr(
#         model,
#         'ROOT_FOLDER',
#         f'{TEST_ROOT_FOLDER}{model.ROOT_FOLDER}',
#         raising=True
#     )
#     return model
#
#
# @pytest.mark.parametrize('command', [create_page, create_template])
# def test_common_create_commands(command, ):
#     command_result = CliRunner().invoke(command, RELATIVE_PATH_A)
#     assert command_result.exit_code == 0
#
#
# @pytest.mark.parametrize('command', [delete_page, delete_template])
# def test_common_delete_commands(command):
#     command_result = CliRunner().invoke(command, RELATIVE_PATH_A)
#     assert command_result.exit_code == 0
