from engine.models.files.bases.file import File


class Processor:
    @classmethod
    def _get_file_path(cls, file):
        return file.absolute_path

    @classmethod
    def _process(cls, content):
        raise NotImplementedError('Can\'t call abstract `_process`. Override it')

    @classmethod
    def _read_original_content(cls, file):
        original_file = File(file.absolute_path)
        original_content = original_file.read()
        return original_content

    @classmethod
    def _write_processed_content(cls, file, processed_content):
        processed_file_path = cls._get_file_path(file)
        processed_file = File(processed_file_path)
        processed_file.write(processed_content)
        return processed_file

    @classmethod
    def process_content(cls, content):
        return cls._process(content)

    @classmethod
    def process_file(cls, file):
        original_content = cls._read_original_content(file)
        processed_content = cls.process_content(original_content)
        processed_file = cls._write_processed_content(file, processed_content)
        return processed_file
