from bs4 import BeautifulSoup

from legacy.extensions.highlighter import highlight_precode
from engine.models.processors.bases.processor import Processor


class Highlighter(Processor):
    @classmethod
    def _process(cls, content):
        soup = BeautifulSoup(content, features='html.parser')
        return str(highlight_precode(soup))
