import pytest

from engine.tests.conftest import TEST_ROOT
from engine.models.files.bases.file import File
from engine.models.processors.minifier import Minifier


def test_process_minifies_html():
    test_html = '  <p>yolo<a  href="/" >o </a >     <!-- hello --></p>'
    assert Minifier._process(test_html) == '<p>yolo<a href="/" >o </a > </p>'


@pytest.mark.parametrize(
    'original_file_path, expected_processed_path',
    [[f'{TEST_ROOT}/page.html', f'{TEST_ROOT}/page.min.html']]
)
def test_get_processed_file_path(original_file_path, expected_processed_path):
    file = File(original_file_path)
    assert Minifier._get_processed_file_path(file) == expected_processed_path
