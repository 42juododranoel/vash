import pytest

from engine.models.file import File
from engine.models.folder import Folder
from engine.models.resource import Resource
from engine.models.resources.page import Page
from engine.models.resources.template import Template

NODE_SUBCLUSSES = [File, Folder, Resource, Template, Page]

NODE_PATHS = [
    '/tmp/the-holy-grail/french-castle/trojan-badger',
    '/tmp/the-holy-grail/the-black-knight',
]

RESOURCE_PATHS_SETS = [
    ['tests/the-holy-grail/french-castle/trojan-badger', 'tests/the-holy-grail/the-black-knight'],
    ['tests/the-black-knight'],
]


@pytest.fixture
def initialize_and_create():
    instances = []

    def _initialize_and_create(model, *args, **kwargs):
        instance = model(*args, **kwargs)
        instance.create()
        instances.append(instance)
        return instance

    yield _initialize_and_create

    for instance in instances:
        instance.delete()


@pytest.fixture(params=NODE_PATHS)
def node_path(request):
    return request.param


file_path = node_path
