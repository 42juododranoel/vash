from new_engine.command.models import AbstractCommand
from new_engine.page.models import Page


class BasePageCommand(AbstractCommand):
    def get_parser(self):
        parser = super().get_parser()
        parser.add_argument('path', help='Page path.')
        return parser


class CreatePageCommand(BasePageCommand):
    def execute(self, path):
        page = Page(path)
        page.validate()
        page.create()


class DeletePageCommand(BasePageCommand):
    def execute(self, path):
        page = Page(path)
        page.validate()
        page.delete()


class RepathPageCommand(BasePageCommand):
    def get_parser(self):
        parser = super().get_parser()
        parser.add_argument('new_path', help='New page path.')
        return parser

    def execute(self, path, new_path):
        page = Page(path)
        page.validate()
        page.validate_path(new_path)
        page.rename(new_path)


command_switch = {
    'create-page': CreatePageCommand,
    'delete-page': DeletePageCommand,
    'rename-page': RepathPageCommand,
}

command_switch['make-page'] = command_switch['create-page']
command_switch['prepare-page'] = command_switch['create-page']

command_switch['remove-page'] = command_switch['delete-page']
