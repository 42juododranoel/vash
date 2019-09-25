from argparse import ArgumentParser


class AbstractCommand:
    def __init__(self, arguments):
        self.parser = self.get_parser()
        self.arguments = arguments

    def get_parser(self):
        return ArgumentParser()

    def dispatch(self):
        parsed_arguments = self.parser.parse_args(self.arguments)
        return self.execute(**vars(parsed_arguments))

    def execute(self):
        raise NotImplementedError(_('Can\'t execute abstract command.'))
