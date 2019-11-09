from engine.models.files._.file import File

from jinja2 import Markup, Template


class HtmlFile(File):
    def render(self, context):
        with open(self.absolute_path) as file:
            file_content = file.read()
            jinja_file = Template(file_content)
        return Markup(jinja_file.render(**context))
