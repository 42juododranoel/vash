import pytest

from new_engine.models.resource import Resource
from new_engine.tests.conftest import (
    NODE_SUBCLUSSES,
    # NODE_NEW_PATH
)


@pytest.fixture
def resource(request, node_path):
    resource = Resource(node_path)
    yield resource
    resource.delete()


@pytest.fixture
def created_resource(request, node_path):
    resource = Resource(node_path)
    resource.create()
    yield resource
    resource.delete()


@pytest.fixture
def moved_resource(request, node_path, node_new_path):
    resource = Resource(node_path)
    resource.create()
    resource.move(node_new_path)
    yield resource
    resource.delete()
    resource_before_moving = Resource(node_path)
    resource_before_moving.delete()
