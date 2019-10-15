from shutil import rmtree
from os.path import isdir

import pytest

from engine.models.files.file import File
from engine.models.files.json_file import JsonFile
from engine.models.files.meta_file import MetaFile
from engine.models.files.page_meta_file import PageMetaFile
from engine.models.files.template_meta_file import TemplateMetaFile
from engine.models.node import Node
from engine.models.folder import Folder
from engine.models.resource import Resource
from engine.models.resources.page import Page
from engine.models.resources.template import Template

TESTS_ROOT_FOLDER = '/tmp/tests'

FOLDER_AND_SUBCLASSES = [Folder]

FILE_SUBCLASSES = [JsonFile, MetaFile, PageMetaFile, TemplateMetaFile]
FILE_AND_SUBCLASSES = [File] + FILE_SUBCLASSES

RESOURCE_SUBCLASSES = [Page, Template]
RESOURCE_AND_SUBCLASSES = [Resource] + RESOURCE_SUBCLASSES

NODE_SUBCLASSES = FILE_AND_SUBCLASSES+ FOLDER_AND_SUBCLASSES + RESOURCE_AND_SUBCLASSES
NODE_AND_SUBCLASSES = [Node] + NODE_SUBCLASSES

NODE_PATHS = [
    f'{TESTS_ROOT_FOLDER}/the-holy-grail/french-castle/trojan-badger',
    f'{TESTS_ROOT_FOLDER}/the-holy-grail/the-black-knight',
]
NODE_NEW_PATHS = NODE_PATHS[::-1]

RESOURCE_PATHS = [
    'tests/the-holy-grail/french-castle/trojan-badger',
    'tests/the-holy-grail/the-black-knight',
]
RESOURCE_NEW_PATHS = RESOURCE_PATHS[::-1]


@pytest.fixture(autouse=True)
def remove_test_folder(request):
    yield
    if isdir(TESTS_ROOT_FOLDER):
        rmtree(TESTS_ROOT_FOLDER)


@pytest.fixture
def create():
    def _create(model, *args, **kwargs):
        instance = model(*args, **kwargs)
        instance.create()
        return instance

    return _create


@pytest.fixture(params=NODE_PATHS)
def node_path(request):
    return request.param


@pytest.fixture(params=NODE_NEW_PATHS)
def node_new_path(request):
    return request.param


@pytest.fixture(params=RESOURCE_PATHS)
def resource_path(request):
    return request.param


@pytest.fixture(params=RESOURCE_NEW_PATHS)
def resource_new_path(request):
    return request.param


# TODO: Figure out how to get rid of it
file_path = node_path
folder_path = node_path
