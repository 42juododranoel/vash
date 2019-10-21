import os

from click import echo


class Node:
    ROOT_FOLDER = ''

    def __init__(self, path):
        self.path = path
        self.name = path.split('/')[-1]

    @property
    def is_present(self):
        return self._check_presence(self.absolute_path)

    @property
    def absolute_path(self):
        return self.path if self.path.startswith('/') \
            else f'{self.ROOT_FOLDER}/{self.path}'

    def create(self):
        if not self.is_present:
            echo(f'Create “{self.path}”')
            parent = '/'.join(self.absolute_path.split('/')[:-1])
            if parent:  # `parent` is '' if `path` is 'plain', no 'hie/rar/chy'
                os.makedirs(parent, exist_ok=True)
            self._create(self.absolute_path)

    def delete(self):
        if self.is_present:
            echo(f'Delete “{self.path}”')
            self._delete(self.absolute_path)
