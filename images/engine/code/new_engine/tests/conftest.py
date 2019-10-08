import pytest

from new_engine.models.page import Page
from new_engine.models.template import Template
from new_engine.models.resource import Resource
from new_engine.models.file import File
from new_engine.models.folder import Folder

NODE_SUBCLUSSES = [File, Folder, Resource, Template, Page]

TEST_NODE_PATH = '/tmp/the-holy-grail/french-castle/trojan-badger'
TEST_NODE_NEW_PATH = '/tmp/the-holy-grail/the-black-knight'
TEST_NODE_PATHS = [TEST_NODE_PATH, TEST_NODE_NEW_PATH]

TEST_RESOURCE_PATH = TEST_NODE_PATH
TEST_RESOURCE_NEW_PATH = TEST_NODE_NEW_PATH

TEST_PAGE_PATH = 'the-holy-grail/french-castle/trojan-badger'
TEST_PAGE_NEW_PATH = 'the-holy-grail/the-holy-hand-grenade-of-antioch'
TEST_TEMPLATE_PATHS = [TEST_PAGE_PATH, TEST_PAGE_NEW_PATH]

TEST_TEMPLATE_PATH = TEST_PAGE_PATH
TEST_TEMPLATE_NEW_PATH = TEST_PAGE_NEW_PATH
TEST_TEMPLATE_PATHS = [TEST_TEMPLATE_PATH, TEST_TEMPLATE_NEW_PATH]

TEST_FILE_PATH = '/tmp/the-holy-grail/the-holy-hand-grenade-of-antioch.txt'
TEST_FOLDER_PATH = '/tmp/the-holy-grail/the-holy-hand-grenade-of-antioch'


@pytest.fixture
def file(request):
    file = File(TEST_FILE_PATH)
    yield file
    file.delete()


@pytest.fixture
def folder(request):
    folder = Folder(TEST_FOLDER_PATH)
    yield folder
    folder.delete()


@pytest.fixture(params=[Resource, Page, Template])
def resource(request):
    resource = request.param(TEST_RESOURCE_PATH)
    yield resource
    resource.delete()
