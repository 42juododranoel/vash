import os

import pytest


class TestCommonResourceMethods:
    # TODO: Move deletes old folders

    def test_attributes_after_initializing(self, resource):
        assert resource.files.keys() == resource._get_files().keys()

    def test_create_creates_files(self, created_resource):
        for _, file in created_resource.files.items():
            assert file.is_present

    def test_move_moves_files(self, moved_resource):
        new_name = moved_resource.path.rpartition('/')[-1]
        for _, file in moved_resource.files.items():
            assert file.is_present
            assert new_name == file.name.rsplit('.')[0]
