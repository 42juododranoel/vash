from jinja2 import (
    Markup,
    Environment,
    FileSystemLoader,
    select_autoescape,
)

from engine.models.files.file import File


def get_environment():
    return Environment(
        loader=FileSystemLoader(['/resources/templates', '/resources/pages']),
        autoescape=select_autoescape(),
    )


class HtmlFile(File):
    def render(self, context):
        environment = get_environment()
        # TODO: Rewrite with `node` later
        # block HACK
        path = self.path
        path = path.replace('/resources/templates/', '')
        path = path.replace('/resources/pages/', '')
        # endblock HACK
        template = environment.get_template(path)
        return Markup(template.render(**context))
