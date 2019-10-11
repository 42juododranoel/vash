from css_html_js_minify import html_minify

from engine.models.processor import Processor


class Minifier(Processor):
    @staticmethod
    def process_content(content):
        return html_minify(content)
