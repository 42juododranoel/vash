from css_html_js_minify import html_minify

from engine.models.processors.processor import Processor


class Minifier(Processor):
    @classmethod
    def get_file_path(cls, file):
        name, dot, extension = file.name.rpartition('.')
        new_name = f'{name}.min.{extension}'
        parent, slash_if_present, name = file.path.rpartition('/')
        return f'{parent}{slash_if_present}{new_name}'

    @classmethod
    def _process(cls, content):
        return html_minify(content)
