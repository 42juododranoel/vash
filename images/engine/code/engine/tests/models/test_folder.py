from engine.models.folder import Folder


def test_is_empty_true_when_empty(create, folder_path):
    folder = create(Folder, folder_path)
    assert folder.is_empty


def test_is_empty_false_when_populated(create, folder_path):
    folder = create(Folder, folder_path)
    with open(f'{folder.path}/test.txt', 'w') as file:
        file.write('')
    assert not folder.is_empty
