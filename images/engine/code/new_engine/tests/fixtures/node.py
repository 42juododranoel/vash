import pytest

from new_engine.tests.conftest import (
    NODE_PATHS,
    NODE_SUBCLUSSES,
    # NODE_NEW_PATH,
)


@pytest.fixture(params=NODE_PATHS)
def node_path(request):
    return request.param


@pytest.fixture(params=NODE_PATHS[::-1])
def node_new_path(request):
    return request.param


@pytest.fixture(params=NODE_SUBCLUSSES)
def node(request, node_path):
    node = request.param(node_path)
    yield node
    node.delete()


@pytest.fixture(params=NODE_SUBCLUSSES)
def created_node(request, node_path):
    node = request.param(node_path)
    node.create()
    yield node
    node.delete()


@pytest.fixture(params=NODE_SUBCLUSSES)
def moved_node(request, node_path, node_new_path):
    node = request.param(node_path)
    node.create()
    node.move(node_new_path)
    yield node
    node.delete()
    node_before_moving = request.param(node_path)
    node_before_moving.delete()
