from bs4 import BeautifulSoup

from legacy.extensions.hanginator import wrap_hanging_punctuation
from engine.models.processors.bases.processor import Processor


class Hanginator(Processor):
    @classmethod
    def _process(cls, content):
        soup = BeautifulSoup(content, features='html.parser')
        return str(wrap_hanging_punctuation(soup))
