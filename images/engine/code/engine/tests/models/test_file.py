from engine.models.file import File

# TODO: test write writes when present
# TODO: test write creates and writes when missing
# TODO: test write writes content
# TODO: test write writes binary content
# TODO: test read reads content
# TODO: test read reads binary content


def test_create_creates_with_initial_content(initialize_and_create, file_path):
    created_file = initialize_and_create(File, file_path)
    with open(created_file.path) as file_on_disk:
        assert file_on_disk.read() == created_file._get_initial_content()
