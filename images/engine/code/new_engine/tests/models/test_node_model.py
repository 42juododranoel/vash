import os

import pytest

from new_engine.tests.conftest import (
    TEST_NODE_PATH,
    TEST_NODE_NEW_PATH,
)


class TestCommonNodeMethods:
    def test_attributes_after_initializing(self, node):
        assert node.path == TEST_NODE_PATH
        assert node.name == TEST_NODE_PATH.split('/')[-1]
        assert node.parent == '/'.join(TEST_NODE_PATH.split('/')[:-1])

    def test_is_present_true_when_present(self, present_node):
        assert present_node.is_present

    def test_is_present_false_when_missing(self, node):
        assert not node.is_present

    def test_create_idles_when_present(self, present_node):
        assert present_node.is_present
        present_node.create()

    def test_create_creates_when_missing(self, node):
        assert not node.is_present
        node.create()
        assert node.is_present

    def test_delete_deletes_when_present(self, present_node):
        assert present_node.is_present
        present_node.delete()
        assert not present_node.is_present

    def test_delete_idles_when_missing(self, node):
        assert not node.is_present
        node.delete()

    def test_move_moves_when_present(self, present_node):
        assert present_node.is_present
        old_path = present_node.path
        present_node.move(TEST_NODE_NEW_PATH)
        assert present_node.is_present
        assert not present_node._check_presence(old_path)

    def test_move_idles_when_missing(self, node):
        assert not node.is_present
        node.move(TEST_NODE_NEW_PATH)
