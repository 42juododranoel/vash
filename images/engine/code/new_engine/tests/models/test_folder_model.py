class TestFolder:
    def test_is_empty_true_when_empty(self, folder):
        folder.create()
        assert folder.is_empty

    def test_is_empty_false_when_populated(self, folder):
        folder.create()
        with open(f'{folder.path}/test.txt', 'w') as file:
            file.write('')
        assert not folder.is_empty
