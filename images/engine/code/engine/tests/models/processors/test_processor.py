import pytest

from engine.models.processors.processor import Processor


# TODO: test all child models share similar interface

def test_process_content_method_is_abstract():
    processor = Processor()
    pytest.raises(NotImplementedError, processor.process_content, None)


def test_process_file_method_is_abstract():
    processor = Processor()
    pytest.raises(NotImplementedError, processor.process_file, None)
