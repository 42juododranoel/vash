from engine.models.resources.page import Page
from engine.commands.page import create_page, delete_page

# TODO: Think on how to rewrite it flat
# TODO: Test both `Page` and `Template` commands near

# TODO: test create when created
# TODO: test delete when not created

# def test_create_creates_when_not_created(cli_runner, resource_paths):
#     create_command_result = cli_runner.invoke(create_page, resource_paths)
#     assert create_command_result.exit_code == 0
#
#     for resource_path in resource_paths:
#         page = Page(resource_path)
#         assert page.is_present
#
#
# def test_delete_deletes_when_created(cli_runner, created_resource_paths):
#     for resource_path in created_resource_paths:
#         page = Page(resource_path)
#         assert page.is_present
#
#     delete_command_result = cli_runner.invoke(delete_page, created_resource_paths)
#     assert delete_command_result.exit_code == 0
#
#     for resource_path in created_resource_paths:
#         page = Page(resource_path)
#         assert not page.is_present

# import pytest
# from click.testing import CliRunner
#
# from engine.tests.conftest import RESOURCE_PATHS_SETS
# from engine\.models\.resources\.resource\  import Resource

# TODO: Think on how to move it to conftest properly


# @pytest.fixture
# def cli_runner():
#     return CliRunner()
#
#
# @pytest.fixture(params=RESOURCE_PATHS_SETS)
# def resource_paths_set(request):
#     return request.param
#
#
# @pytest.fixture
# def resource_paths(request, resource_paths_set):
#     yield resource_paths_set
#
#     for resource_path in resource_paths_set:
#         resource = Resource(resource_path)
#         resource.delete()
#
#
# @pytest.fixture
# def created_resource_paths(request, resource_paths_set):
#     for resource_path in resource_paths_set:
#         resource = Resource(resource_path)
#         resource.create()
#
#     yield resource_paths_set
#
#     for resource_path in resource_paths_set:
#         resource = Resource(resource_path)
#         resource.delete()
