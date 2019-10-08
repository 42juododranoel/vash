class TestFile:
    def test_create_with_initial_content(self, created_file):
        with open(created_file.path) as file_on_disk:
            assert file_on_disk.read() == created_file._get_initial_content()
