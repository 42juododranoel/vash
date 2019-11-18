import pytest

from engine.models.files.bases.file import File
from engine.models.processors.bases.binary import BinaryProcessor
from engine.models.processors.bases.processor import Processor


@pytest.mark.parametrize('model', [Processor, BinaryProcessor])
def test_get_processed_file_path_returns_absolute_path(model, path):
    file = File(path)
    assert model._get_processed_file_path(file) == file.absolute_path


@pytest.mark.parametrize('model', [Processor, BinaryProcessor])
def test_process_returns_unmodified_content(model):
    content = 'test content'
    assert model._process(content) == content


@pytest.mark.parametrize('model', [Processor, BinaryProcessor])
def test_process_content_simply_content_method(model):
    content = 'test content'
    assert model.process_content(content) == model._process(content)


@pytest.mark.parametrize('model', [Processor, BinaryProcessor])
def test_process_file(model, path):
    content = 'test content'
    file = File(path)
    file.write(content)
    processed_file = Processor.process_file(file)
    assert processed_file.read() == content


def test_read_original_content_reads_from_file(path):
    content = 'test content'
    file = File(path)
    file.write(content)
    assert Processor._read_original_content(file) == file.read()


def test_write_processed_content_writes_to_file(path):
    content = 'test content'
    file = File(path)
    processed_file = Processor._write_processed_content(file, content)
    assert processed_file.read() == content
