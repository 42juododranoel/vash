# import pytest
# from click.testing import CliRunner
#
# from new_engine.commands.template import (
#     create_templates,
#     delete_templates,
#     rename_template,
# )
# from new_engine.tests.conftest import (
#     TEST_TEMPLATE_PATH,
#     TEST_TEMPLATE_NEW_PATH,
#     TEST_TEMPLATE_PATHS,
# )
# from new_engine.models.template import Template
#
# runner = CliRunner()
#
#
# def delete_templates(paths):
#     for path in paths:
#         template = Template(path)
#         template.delete()
#
#
# class TestTemplateCommands:
#     @pytest.mark.parametrize('paths', TEST_TEMPLATE_PATHS)
#     def test_create_creates_templates(self, paths):
#         delete_templates(paths)
#
#         result = runner.invoke(create_templates, paths)
#         assert result.exit_code == 0
#
#         for path in paths:
#             template = Template(path)
#             assert template.is_present
#
#         delete_templates(paths)
#
#     @pytest.mark.parametrize('paths', TEST_TEMPLATE_PATHS)
#     def test_delete_deletes_templates(self, paths):
#         delete_templates(paths)
#
#         create_result = runner.invoke(create_templates, paths)
#         delete_result = runner.invoke(delete_templates, paths)
#         assert delete_result.exit_code == 0
#
#         for path in paths:
#             template = Template(path)
#             assert not template.is_present
#
#         delete_templates(paths)
#
#     def test_rename_renames_template(self):
#         delete_templates([TEST_TEMPLATE_PATH, TEST_TEMPLATE_NEW_PATH])
#
#         create_result = runner.invoke(create_templates, TEST_TEMPLATE_PATH)
#         rename_result = runner.invoke(rename_template, [TEST_TEMPLATE_PATH, TEST_TEMPLATE_NEW_PATH])
#         assert rename_result.exit_code == 0
#
#         old_template = Template(TEST_TEMPLATE_PATH)
#         assert not old_template.is_present
#
#         new_template = Template(TEST_TEMPLATE_NEW_PATH)
#         assert new_template.is_present
#
#         delete_templates([TEST_TEMPLATE_PATH, TEST_TEMPLATE_NEW_PATH])
