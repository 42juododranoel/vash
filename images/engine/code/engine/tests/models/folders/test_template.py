import pytest

from engine.models.folders.template import Template


@pytest.fixture(params=[Template])
def model(request, capybara_patch):
    return capybara_patch(request.param)


@pytest.mark.parametrize('file_name', ['meta'])
def test_get_files_has_required_files(model, path, file_name):
    template = model(path)
    assert file_name in template._get_files()
