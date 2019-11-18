from engine.models.files.bases.file import File
from engine.models.files.bases.binary import BinaryFile
from engine.models.processors.bases.binary import BinaryProcessor


def test_read_original_content_reads_binary_from_file(path):
    content = 'test content'
    file = File(path)
    file.write(content)
    binary_content = bytes(content, 'utf8')
    assert BinaryProcessor._read_original_content(file) == binary_content


def test_write_processed_content_writes_to_binary_file(path):
    binary_content = bytes('test content', 'utf8')
    file = BinaryFile(path)
    processed_file = BinaryProcessor._write_processed_content(file, binary_content)
    assert processed_file.read() == binary_content
