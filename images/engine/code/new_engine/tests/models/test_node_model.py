import os

import pytest


class TestCommonNodeMethods:
    # TODO: test _get_absolute_path
    # TODO: test __init__
    # TODO: test path
    # TODO: test move to the same folder
    # TODO: test move to upper folder
    # TODO: test move to lower folder ← hard
    # TODO: test move idles when missing

    # is_present

    def test_is_present_true_when_created(self, created_node):
        assert created_node.is_present

    def test_is_present_false_when_not_created(self, node):
        assert not node.is_present

    # create

    def test_create_idles_when_created(self, created_node):
        assert created_node.is_present
        created_node.create()

    def test_create_creates_when_not_created(self, node):
        assert not node.is_present
        node.create()
        assert node.is_present

    # delete

    def test_delete_deletes_when_created(self, created_node):
        assert created_node.is_present
        created_node.delete()
        assert not created_node.is_present

    def test_delete_idles_when_not_created(self, node):
        assert not node.is_present
        node.delete()

    # move

    def test_move_moves_when_created(self, moved_node):
        assert moved_node.is_present
