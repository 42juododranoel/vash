from bs4 import BeautifulSoup
from pygments import highlight
from bs4.element import PreformattedString
from pygments.lexers import get_lexer_by_name

from vash.utils import get_html_formatter


class DontEscapeDammit(PreformattedString):
    """A trick that prevents BeautifulSoup from changing < to &lt;"""
    def output_ready(self, formatter=None):
        self.format_string(self, formatter)
        return self.PREFIX + self + self.SUFFIX


def highlight_precode(html):
    soup = BeautifulSoup(html, 'html.parser')

    for code_tag in soup.find_all('code'):

        language = code_tag.attrs.get('data-language')
        if not language:
            continue
        lexer = get_lexer_by_name(language)

        indent = int(code_tag.attrs.get('data-indent', '0'))
        lines = [line[indent:] for line in code_tag.text.splitlines()]
        content = '\r\n'.join(lines)

        formatter = get_html_formatter()
        html = highlight(content, lexer, formatter)
        code_tag.replace_with(DontEscapeDammit(html))

    return str(soup)
