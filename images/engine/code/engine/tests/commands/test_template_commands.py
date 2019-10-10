import pytest

from engine.models.resources.template import Template
from engine.commands.template import create_template, delete_template


class TestTemplateCommands:
    # TODO: test create when created
    # TODO: test delete when not created

    def test_create_creates_when_not_created(self, cli_runner, resource_paths):
        create_command_result = cli_runner.invoke(create_template, resource_paths)
        assert create_command_result.exit_code == 0

        for resource_path in resource_paths:
            template = Template(resource_path)
            assert template.is_present

    def test_delete_deletes_when_created(self, cli_runner, resource_paths):
        for resource_path in resource_paths:
            template = Template(resource_path)
            assert template.is_present

        delete_command_result = cli_runner.invoke(delete_template, resource_paths)
        assert delete_command_result.exit_code == 0

        for resource_path in resource_paths:
            template = Template(resource_path)
            assert not template.is_present
