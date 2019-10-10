from brotli import compress, MODE_GENERIC


def compress_file(path):
    path_compressed = path + '.br'
    with open(path_compressed, 'wb') as file_compressed:
        with open(path, 'rb') as file:
            compressed_content = compress(
                file.read(),
                mode=MODE_GENERIC,
                quality=11,
                lgwin=22,
                lgblock=0,
            )
        file_compressed.write(compressed_content)
    return path_compressed
