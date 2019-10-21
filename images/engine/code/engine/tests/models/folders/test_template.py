import pytest

from engine.models.folders.template import Template
from engine.tests.conftest import TEST_ROOT_FOLDER


@pytest.fixture
def model(monkeypatch):
    model = Template
    monkeypatch.setattr(
        model,
        'ROOT_FOLDER',
        f'{TEST_ROOT_FOLDER}{model.ROOT_FOLDER}',
        raising=True
    )
    return model


@pytest.mark.parametrize('key', ['meta'])
def test_get_files_has_keys(model, path, key):
    template = model(path)
    assert key in template._get_files()


def test_get_meta_reads_meta(model, path):
    template = model(path)
    template.create()

    test_content = 'foo bar 42'
    template.files['meta'].write(test_content)

    meta = template.get_meta()
    assert meta == test_content
