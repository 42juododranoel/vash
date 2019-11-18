from engine.models.folders.template import Template
from engine.models.files.bases.file import File

from jinja2 import Markup, Environment, FileSystemLoader, select_autoescape


class HtmlFile(File):
    def render(self, context):
        with open(self.absolute_path) as file:
            file_content = file.read()

        environment = Environment(
            loader=FileSystemLoader(Template.ROOT),
            autoescape=select_autoescape(['html']),
        )
        jinja_file = environment.from_string(file_content)
        return Markup(jinja_file.render(**context))


# from engine.models.files.bases.file import File
#
# from jinja2 import Markup, Template
#
#
# class HtmlFile(File):
#     def render(self, context):
#         with open(self.absolute_path) as file:
#             file_content = file.read()
#             jinja_file = Template(file_content)
#         return Markup(jinja_file.render(**context))
