import pytest

from engine.models.files.bases.file import File
from engine.models.processors.minifier import Minifier


# def test_is_binary_false():
#     assert not Minifier.IS_BINARY
#
#
# def test_process_minifies_html():
#     test_html = '  <p>yolo<a  href="/" >o </a >     <!-- hello --></p>'
#     assert Minifier._process(test_html) == '<p>yolo<a href="/" >o </a > </p>'
#
#
# @pytest.mark.parametrize('file_path, expected_path', [['page.html', 'page.min.html']])
# def test_get_file_path(file_path, expected_path):
#     file = File(file_path)
#     assert Minifier._get_file_path(file) == expected_path
