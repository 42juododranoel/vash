from engine.models.files.file import File
from engine.models.files.binary_file import BinaryFile


class Processor:
    IS_BINARY = False

    @classmethod
    def get_file_path(cls, file):
        return file.path  # Inline by default

    @classmethod
    def _process(cls, content):
        raise NotImplementedError('Can\'t call abstract `_process`, override it')

    @classmethod
    def process_content(cls, content):
        return cls._process(content)

    @classmethod
    def process_file(cls, file):
        path = cls.get_file_path(file)

        file_model = BinaryFile if cls.IS_BINARY else File
        processed_file = file_model(path)

        original_content = file.read()
        compressed_content = cls.process_content(original_content)
        processed_file.write(compressed_content)

        return processed_file
