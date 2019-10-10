import pytest


class TestCommonProcessorMethods:
    def test_process_content(self, processor):
        pytest.raises(NotImplementedError, processor.process_content, '')


class TestMinifier:
    def test_minifies_html(self, minifier):
        test_html = '  <p>yolo<a  href="/" >o </a >     <!-- hello --></p>'
        assert minifier.process_content(test_html) == '<p>yolo<a href="/" >o </a > </p>'
