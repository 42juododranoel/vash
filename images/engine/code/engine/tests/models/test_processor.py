import pytest


class TestCommonProcessorMethods:
    # TODO: test all child models share similar interface

    def test_process_content_method_is_abstract(self, processor):
        pytest.raises(NotImplementedError, processor.process_content, None)

    def test_process_file_method_is_abstract(self, processor):
        pytest.raises(NotImplementedError, processor.process_file, None)


class TestMinifier:
    def test_minifies_html(self, minifier):
        test_html = '  <p>yolo<a  href="/" >o </a >     <!-- hello --></p>'
        assert minifier.process_content(test_html) == '<p>yolo<a href="/" >o </a > </p>'
