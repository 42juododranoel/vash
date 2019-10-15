class Processor:
    @staticmethod
    def process_content(content):
        raise NotImplementedError('Can\'t call abstract `process_content`')

    @staticmethod
    def process_file(file):
        raise NotImplementedError('Can\'t call abstract `process_file`')
