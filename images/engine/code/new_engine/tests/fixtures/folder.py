import pytest

from new_engine.models.folder import Folder


@pytest.fixture
def created_folder(request, node_path):
    folder = Folder(node_path)
    folder.create()
    yield folder
    folder.delete()
