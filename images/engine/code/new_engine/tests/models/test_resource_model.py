import os

import pytest

from new_engine.tests.conftest import TEST_RESOURCE_NEW_PATH


class TestCommonResourceMethods:
    def test_attributes_after_initializing(self, resource):
        assert resource.files.keys() == resource._get_files().keys()

    def test_create_creates_files(self, resource):
        resource.create()
        for _, file in resource.files.items():
            assert file.is_present

    def test_move_moves_files(self, resource):
        resource.create()
        resource.move(TEST_RESOURCE_NEW_PATH)
        new_name = TEST_RESOURCE_NEW_PATH.rpartition('/')[-1]
        for _, file in resource.files.items():
            assert file.is_present
            assert new_name == file.name.rsplit('.')[0]

    def test_move_deletes_empty_folders(self, resource):
        resource.create()
        old_parent = resource.parent
        resource.move(TEST_RESOURCE_NEW_PATH)
        assert not os.path.isdir(old_parent)
