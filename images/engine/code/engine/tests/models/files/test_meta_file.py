import pytest

from engine.models.files.meta import MetaFile


@pytest.fixture(params=[MetaFile])
def model(request):
    return request.param


def test_has_no_default_keys(model, path):
    meta_file = model(path)
    assert not meta_file.INITIAL_KEYS
