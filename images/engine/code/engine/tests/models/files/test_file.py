import pytest

from engine.tests.conftest import FILE_AND_SUBCLUSSES

# TODO: test write writes when present
# TODO: test write creates and writes when missing
# TODO: test write writes content
# TODO: test write writes binary content
# TODO: test read reads content
# TODO: test read reads binary content


@pytest.mark.parametrize('model', FILE_AND_SUBCLUSSES)
def test_create_creates_with_initial_content(create, model, file_path):
    created_file = create(model, file_path)
    with open(created_file.path) as file_on_disk:
        assert file_on_disk.read() == created_file._get_initial_content()
