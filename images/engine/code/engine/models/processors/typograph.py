from richtypo import Richtypo

from engine.models.processors.processor import Processor


class RichtypoBypassingStyleTag(Richtypo):
    bypass_tags = Richtypo.bypass_tags + ['style']


class Typograph(Processor):
    @classmethod
    def _get_file_path(cls, file):
        return file.absolute_path

    @classmethod
    def _process(cls, content):
        richtypo = RichtypoBypassingStyleTag('ru-lite')
        return richtypo.richtypo(content)
