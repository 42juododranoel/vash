import string

import pytest

from engine.models.files._.file import File
from engine.models.processors.brotler import Brotler


# def test_is_binary_true():
#     assert Brotler.IS_BINARY
#
#
# def test_process_compresses_text():
#     content = bytes(string.printable + string.printable, 'utf8')
#     assert Brotler._process(content) == b"""\x1b\xc7\x00\xf8\x1d\x89\xb1\x8d\x8a}u@\x11\xd2\x97&\xd7\xe5\xa9\x84\x85\xb6\x832\xf8r\xfbqs\xa92\xf3Q\xf1Q\xaa]J\xb5\xc5c\xcc#\xeeg\x06\x8e1\x87\xf0\xccs!\x956\xd6\xfd7\x12\x8b\x9a\xf3!\xa6\\j\xebc\xae}\xee\xfb\xd0}\x88)\x97\xda\xfa0N\xf3\xb2n\xfbq^\xf7\xf3~\x14"L(\xe3B*m\xac\x0b1\xe5R\xdb\x98k\x1f\xe7\xf3~?\x00\x90 \x0c"""
#
#
# @pytest.mark.parametrize('file_path, expected_path', [['page.html', 'page.html.br']])
# def test_get_file_path(file_path, expected_path):
#     file = File(file_path)
#     assert Brotler.get_file_path(file) == expected_path
