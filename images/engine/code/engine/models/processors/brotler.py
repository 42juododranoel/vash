import brotli

from engine.models.processors.processor import Processor


class Brotler(Processor):
    IS_BINARY = True

    @classmethod
    def get_file_path(cls, file):
        return f'{file.path}.br'

    @classmethod
    def _process(cls, content):
        compressed_content = brotli.compress(
            content,
            mode=brotli.MODE_GENERIC,
            quality=11,
            lgwin=22,
            lgblock=0,
        )
        return compressed_content
