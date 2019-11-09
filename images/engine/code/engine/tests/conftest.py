from shutil import rmtree
from os.path import isdir

import pytest

from engine.models.node import Node
#
from engine.models.folders.page import Page
from engine.models.folders.folder import Folder
from engine.models.folders.template import Template
from engine.models.folders.resource import Resource
#
from engine.models.files.file import File
from engine.models.files.json_file import JsonFile
from engine.models.files.meta_file import MetaFile
from engine.models.files.page_meta_file import PageMetaFile
from engine.models.files.template_meta_file import TemplateMetaFile
#
from engine.models.processors.brotler import Brotler
from engine.models.processors.minifier import Minifier
from engine.models.processors.processor import Processor

TEST_ROOT_FOLDER = '/tmp/tests'

RELATIVE_PATH_A = 'the-holy-grail/french-castle'
RELATIVE_PATH_B = 'the-holy-grail/the-black-knight'

ABSOLUTE_PATH_A = f'{TEST_ROOT_FOLDER}/{RELATIVE_PATH_A}'
ABSOLUTE_PATH_B = f'{TEST_ROOT_FOLDER}/{RELATIVE_PATH_B}'

FILE_SUBCLASSES = [JsonFile]
JSON_FILE_SUBCLASSES = [MetaFile]
META_FILE_SUBCLASSES = [PageMetaFile, TemplateMetaFile]
FILE_CLASSES = [File] + FILE_SUBCLASSES + JSON_FILE_SUBCLASSES + META_FILE_SUBCLASSES

RESOURCE_SUBCLASSES = [Page, Template]
RESOURCE_CLASSES = [Resource] + RESOURCE_SUBCLASSES

FOLDER_CLASSES = [Folder] + RESOURCE_CLASSES

NODE_SUBCLASSES = FILE_CLASSES + FOLDER_CLASSES
NODE_CLASSES = [Node] + NODE_SUBCLASSES

PROCESSOR_SUBCLASSES = [Minifier]
PROCESSOR_CLASSES = [Processor] + PROCESSOR_SUBCLASSES


@pytest.fixture(autouse=True)
def monkey_patch_node_root_folder(monkeypatch):
    for model in NODE_CLASSES:
        monkeypatch.setattr(
            model,
            'ROOT_FOLDER',
            f'{TEST_ROOT_FOLDER}{model.ROOT_FOLDER}',
            raising=True
        )


@pytest.fixture(autouse=True)
def remove_node_root_folder(request):
    yield
    if isdir(TEST_ROOT_FOLDER):
        rmtree(TEST_ROOT_FOLDER)


@pytest.fixture
def relative_path():
    return RELATIVE_PATH_A


@pytest.fixture
def absolute_path():
    return ABSOLUTE_PATH_A


@pytest.fixture(params=[RELATIVE_PATH_A] + [ABSOLUTE_PATH_A])
def path(request):
    return request.param
