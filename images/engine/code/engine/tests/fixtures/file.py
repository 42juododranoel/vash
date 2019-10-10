import pytest

from engine.models.file import File
from engine.models.files.json_file import JsonFile
from engine.models.files.meta_file import MetaFile
from engine.models.files.page_meta_file import PageMetaFile
from engine.models.files.template_meta_file import TemplateMetaFile


@pytest.fixture
def created_file(request, node_path):
    file = File(node_path)
    file.create()
    yield file
    file.delete()


@pytest.fixture
def created_json_file(request, node_path):
    file = JsonFile(node_path)
    file.create()
    yield file
    file.delete()


@pytest.fixture
def created_meta_file(request, node_path):
    file = MetaFile(node_path)
    file.create()
    yield file
    file.delete()


@pytest.fixture
def template_meta_file(request, node_path):
    file = TemplateMetaFile(node_path)
    file.create()
    yield file
    file.delete()


@pytest.fixture
def page_meta_file(request, node_path):
    file = PageMetaFile(node_path)
    file.create()
    yield file
    file.delete()
