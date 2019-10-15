import pytest

from engine.models.files.file import File
from engine.models.files.json_file import JsonFile
from engine.models.files.meta_file import MetaFile
from engine.models.files.page_meta_file import PageMetaFile
from engine.models.files.template_meta_file import TemplateMetaFile
from engine.models.folder import Folder
from engine.models.resource import Resource
from engine.models.resources.page import Page
from engine.models.resources.template import Template

NODE_SUBCLUSSES = [File, Folder, Resource, Template, Page]

FILE_AND_SUBCLUSSES = [File, JsonFile, MetaFile, PageMetaFile, TemplateMetaFile]

NODE_PATHS = [
    '/tmp/the-holy-grail/french-castle/trojan-badger',
    '/tmp/the-holy-grail/the-black-knight',
]

RESOURCE_PATHS_SETS = [
    ['tests/the-holy-grail/french-castle/trojan-badger', 'tests/the-holy-grail/the-black-knight'],
    ['tests/the-black-knight'],
]


@pytest.fixture
def create():
    created_instances = []

    def _create(model, *args, **kwargs):
        instance = model(*args, **kwargs)
        instance.create()
        created_instances.append(instance)
        return instance

    yield _create

    for instance in created_instances:
        instance.delete()


@pytest.fixture(params=NODE_PATHS)
def node_path(request):
    return request.param


file_path = node_path
folder_path = node_path
