import pytest

from engine.models.files.meta_file import MetaFile


@pytest.fixture(params=[MetaFile])
def model(request, capybara_patch):
    return capybara_patch(request.param)


def test_has_no_default_keys(model, path):
    meta_file = model(path)
    assert not meta_file.DEFAULT_KEYS
