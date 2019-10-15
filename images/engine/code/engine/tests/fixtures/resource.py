import pytest

from engine.tests.conftest import RESOURCE_PATHS_SETS
from engine.models.resource import Resource


@pytest.fixture
def moved_resource(request, node_path, node_new_path):
    resource = Resource(node_path)
    resource.create()
    resource.move(node_new_path)
    yield resource

    resource.delete()
    resource_before_moving = Resource(node_path)
    resource_before_moving.delete()


@pytest.fixture(params=RESOURCE_PATHS_SETS)
def resource_paths_set(request):
    return request.param


@pytest.fixture
def resource_paths(request, resource_paths_set):
    yield resource_paths_set

    for resource_path in resource_paths_set:
        resource = Resource(resource_path)
        resource.delete()


@pytest.fixture
def created_resource_paths(request, resource_paths_set):
    for resource_path in resource_paths_set:
        resource = Resource(resource_path)
        resource.create()

    yield resource_paths_set

    for resource_path in resource_paths_set:
        resource = Resource(resource_path)
        resource.delete()
