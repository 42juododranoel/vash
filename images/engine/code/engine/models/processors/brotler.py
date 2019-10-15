import brotli

from engine.models.files.file import File
from engine.models.processors.processor import Processor


class Brotler(Processor):
    @staticmethod
    def process_content(binary_content):
        compressed_content = brotli.compress(
            binary_content,
            mode=brotli.MODE_GENERIC,
            quality=11,
            lgwin=22,
            lgblock=0,
        )
        return compressed_content

    @staticmethod
    def process_file(file):
        compressed_file = File(f'{file.path}.br')

        original_content = file.read(is_binary=True)
        compressed_content = Brotler.process_content(original_content)
        compressed_file.write(compressed_content)

        return compressed_file
