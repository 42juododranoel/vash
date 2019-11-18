from engine.models.files.bases.file import File
from engine.models.files.bases.binary import BinaryFile
from engine.models.processors.bases.processor import Processor


class BinaryProcessor(Processor):
    @classmethod
    def _read_original_content(cls, file):
        original_file = File(file.absolute_path)
        original_content = original_file.read()  # must return string
        binary_content = bytes(original_content, 'utf8')
        return binary_content

    @classmethod
    def _write_processed_content(cls, file, processed_content):
        processed_file_path = cls._get_processed_file_path(file)
        processed_file = BinaryFile(processed_file_path)
        processed_file.write(processed_content)
        return processed_file
