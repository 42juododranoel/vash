class TestFile:
    def test_create_with_initial_content(self, file):
        file.create()
        with open(file.path) as file_on_disk:
            assert file_on_disk.read() == file._get_initial_content()
