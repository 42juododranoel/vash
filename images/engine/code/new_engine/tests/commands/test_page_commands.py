import pytest

from new_engine.models.resources.page import Page
from new_engine.commands.page import create_page, delete_page


class TestPageCommands:
    # TODO: test create when created
    # TODO: test delete when not created

    def test_create_creates_when_not_created(self, cli_runner, resource_paths):
        create_command_result = cli_runner.invoke(create_page, resource_paths)
        assert create_command_result.exit_code == 0

        for resource_path in resource_paths:
            page = Page(resource_path)
            assert page.is_present

    def test_delete_deletes_when_created(self, cli_runner, created_resource_paths):
        for resource_path in created_resource_paths:
            page = Page(resource_path)
            assert page.is_present

        delete_command_result = cli_runner.invoke(delete_page, created_resource_paths)
        assert delete_command_result.exit_code == 0

        for resource_path in created_resource_paths:
            page = Page(resource_path)
            assert not page.is_present
