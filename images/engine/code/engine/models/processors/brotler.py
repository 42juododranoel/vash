import brotli

from engine.models.processors.bases.binary import BinaryProcessor


class Brotler(BinaryProcessor):
    @classmethod
    def _get_processed_file_path(cls, file):
        return f'{file.absolute_path}.br'

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
