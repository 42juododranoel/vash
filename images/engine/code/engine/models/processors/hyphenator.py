from legacy.extensions.hyphenator import hyphenate_html
from engine.models.processors.bases.processor import Processor


class Hyphenator(Processor):
    @classmethod
    def _process(cls, content):
        return hyphenate_html(content)
