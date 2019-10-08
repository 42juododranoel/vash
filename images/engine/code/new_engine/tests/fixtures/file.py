import pytest

from new_engine.models.file import File


@pytest.fixture
def created_file(request, node_path):
    file = File(node_path)
    file.create()
    yield file
    file.delete()
