import re

from bs4.element import PreformattedString

BLACKLISTED_TAGS = [
    '[document]',
    'code', 'tt', 'pre', 'head', 'title', 'script', 'style',
    'meta', 'object', 'embed', 'samp', 'var', 'math', 'select',
    'option', 'input', 'textarea', 'span', 'picture', 'source',
]


class DontEscapeDammit(PreformattedString):
    """A trick that prevents BeautifulSoup from changing < to &lt;"""

    def output_ready(self, formatter=None):
        self.format_string(self, formatter)
        return self.PREFIX + self + self.SUFFIX


def wrapper(match, character):
    result = ''
    if match.group(1):
        result += f'<span class="hanging-{character}-whitespace">{match.group(1)}</span>'
    result += f'<span class="hanging-{character}">{match.group(2)}</span>'
    return result


def wrap_hanging_punctuation(soup):
    strings = soup.findAll(text=lambda text: len(text) > 0)
    for string in strings:
        if string.parent.name not in BLACKLISTED_TAGS:
            laquo_string = re.sub(
                '(\s?)(«)',
                lambda match: wrapper(match, 'laquo'),
                string
            )
            parenthesis_and_laquo_string = re.sub(
                '(\s?)(\()',
                lambda match: wrapper(match, 'lpar'),
                laquo_string
            )
            string.replaceWith(DontEscapeDammit(parenthesis_and_laquo_string))

    return soup
