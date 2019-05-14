import re

from bs4 import BeautifulSoup

BLACKLISTED_TAGS = [
    'code', 'tt', 'pre', 'head', 'title', 'script', 'style',
    'meta', 'object', 'embed', 'samp', 'var', 'math', 'select',
    'option', 'input', 'textarea', 'span', 'picture', 'source',
]


def wrapper(match, character):
    result = ''
    if match.group(1):
        result += f'<span class="{character}-whitespace">{match.group(1)}</span>'
    result += f'<span class="{character}">{match.group(2)}</span>'
    return result


def wrap_hanging_punctuation(html):
    soup = BeautifulSoup(html, 'html.parser')
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
                lambda match: wrapper(match, 'parenthesis'),
                laquo_string
            )
            string.replaceWith(parenthesis_and_laquo_string)

    return str(soup)
