import os

import pytest

from new_engine.tests.conftest import (
    TEST_NODE_PATH,
    TEST_NODE_NEW_PATH,
)


class TestCommonNodeMethods:
    # TODO: test _get_absolute_path
    # TODO: test __init__
    # TODO: test path

    # is_present

    def test_is_present_true_when_present(self, present_node):
        assert present_node.is_present

    def test_is_present_false_when_missing(self, node):
        assert not node.is_present

    # create

    def test_create_idles_when_present(self, present_node):
        assert present_node.is_present
        present_node.create()

    def test_create_creates_when_missing(self, node):
        assert not node.is_present
        node.create()
        assert node.is_present

    # delete

    def test_delete_deletes_when_present(self, present_node):
        assert present_node.is_present
        present_node.delete()
        assert not present_node.is_present

    def test_delete_idles_when_missing(self, node):
        assert not node.is_present
        node.delete()

    # move

    def test_move_moves_when_present(self, moved_node):
        assert moved_node.is_present

    def test_move_idles_when_missing(self, node):
        assert not node.is_present
        node.move(TEST_NODE_NEW_PATH)

    # TODO: test move to the same folder
    # TODO: test move to upper folder
    # TODO: test move to lower folder ← hard
