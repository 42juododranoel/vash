from new_engine.command.models import AbstractCommand
from new_engine.template.models import Template


class BaseTemplateCommand(AbstractCommand):
    def get_parser(self):
        parser = super().get_parser()
        parser.add_argument('name', help='Template name.')
        return parser


class CreateTemplateCommand(BaseTemplateCommand):
    def execute(self, name):
        template = Template(name=name)
        template.validate()
        template.create()


class DeleteTemplateCommand(BaseTemplateCommand):
    def execute(self, name):
        template = Template(name=name)
        template.validate()
        template.delete()


class RenameTemplateCommand(BaseTemplateCommand):
    def get_parser(self):
        parser = super().get_parser()
        parser.add_argument('new_name', help='New template name.')
        return parser

    def execute(self, name, new_name):
        template = Template(name=name)
        template.validate()
        template.validate_name(new_name)
        template.rename(new_name)


command_switch = {
    'create-template': CreateTemplateCommand,
    'delete-template': DeleteTemplateCommand,
    'rename-template': RenameTemplateCommand,
}

command_aliases = {
    'create-template': ['make-template', 'prepare-template'],
    'delete-template': ['remove-template'],
}
for alias, commands in command_aliases.items():
    for command in commands:
        command_switch[command] = command_switch[alias]
