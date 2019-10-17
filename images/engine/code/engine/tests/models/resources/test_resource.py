import pytest

from engine.tests.conftest import RESOURCE_AND_SUBCLASSES

# TODO: test move deletes old folders
# TODO: test root_folder
# TODO: test _get_files
# TODO: test _get_absolute_path


@pytest.mark.parametrize('model', RESOURCE_AND_SUBCLASSES)
def test_create_creates_files(create, model, resource_path):
    resource = create(model, resource_path)
    for _, file in resource.files.items():
        assert file.is_present


@pytest.mark.parametrize('model', RESOURCE_AND_SUBCLASSES)
def test_move_moves_files(create, model, resource_path, resource_new_path):
    resource = create(model, resource_path)
    resource.move(resource_new_path)

    new_name = resource.path.rpartition('/')[-1]
    for _, file in resource.files.items():
        assert file.is_present
        assert new_name == file.name.rsplit('.')[0]
