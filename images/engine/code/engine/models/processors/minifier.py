from css_html_js_minify import html_minify

from engine.models.processors._.processor import Processor


class Minifier(Processor):
    @classmethod
    def _get_file_path(cls, file):
        name, dot, extension = file.name.rpartition('.')
        new_name = f'{name}.min.{extension}'  # filename.html → filename.min.html
        parent, slash_if_present, name = file.absolute_path.rpartition('/')
        return f'{parent}{slash_if_present}{new_name}'

    @classmethod
    def _process(cls, content):
        return html_minify(content)
