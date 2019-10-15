import pytest

from engine.tests.conftest import RESOURCE_AND_SUBCLUSSES

# TODO: test move deletes old folders
# TODO: test root_folder
# TODO: test _get_files
# TODO: test _get_absolute_path


@pytest.mark.parametrize('model', RESOURCE_AND_SUBCLUSSES)
def test_create_creates_files(create, model, resource_path):
    created_resource = create(model, resource_path)
    for _, file in created_resource.files.items():
        assert file.is_present


def test_move_moves_files(moved_resource):
    new_name = moved_resource.path.rpartition('/')[-1]
    for _, file in moved_resource.files.items():
        assert file.is_present
        assert new_name == file.name.rsplit('.')[0]
