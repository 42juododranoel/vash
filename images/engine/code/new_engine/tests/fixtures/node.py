import pytest

from new_engine.tests.conftest import (
    TEST_NODE_PATHS,
    TEST_NODE_NEW_PATH,
    NODE_SUBCLUSSES,
)


@pytest.fixture(params=TEST_NODE_PATHS)
def node_path(request):
    return request.param


@pytest.fixture(params=NODE_SUBCLUSSES)
def node(request, node_path):
    node = request.param(node_path)
    yield node
    node.delete()


@pytest.fixture(params=NODE_SUBCLUSSES)
def present_node(request, node_path):
    node = request.param(node_path)
    node.create()
    yield node
    node.delete()


@pytest.fixture(params=NODE_SUBCLUSSES)
def moved_node(request, node_path):
    node = request.param(node_path)
    node.create()
    node.move(TEST_NODE_NEW_PATH)
    yield node
    node.delete()
