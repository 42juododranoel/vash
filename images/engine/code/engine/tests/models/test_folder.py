from engine.models.folder import Folder


def test_is_empty_true_when_empty(create, folder_path):
    created_folder = create(Folder, folder_path)
    assert created_folder.is_empty


def test_is_empty_false_when_populated(create, folder_path):
    created_folder = create(Folder, folder_path)
    with open(f'{created_folder.path}/test.txt', 'w') as file:
        file.write('')
    assert not created_folder.is_empty
