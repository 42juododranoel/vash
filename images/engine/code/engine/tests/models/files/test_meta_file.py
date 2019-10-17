from engine.models.files.meta_file import MetaFile


def test_has_no_default_keys(create, file_path):
    meta_file = create(MetaFile, file_path)
    assert not meta_file.DEFAULT_KEYS
