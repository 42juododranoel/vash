from bs4 import BeautifulSoup
from pygments import highlight, styles
from bs4.element import PreformattedString
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter

from legacy.constants import _


def get_html_formatter():
    style = styles.get_style_by_name('default')
    formatter = HtmlFormatter(
        style=style,
        linenos='inline',
        classprefix='highlight-',
        cssclass='pre-wrapper highlight-wrapper',
    )
    return formatter


class DontEscapeDammit(PreformattedString):
    """A trick that prevents BeautifulSoup from changing < to &lt;"""
    def output_ready(self, formatter=None):
        self.format_string(self, formatter)
        return self.PREFIX + self + self.SUFFIX


def highlight_precode(soup):
    for code_tag in soup.find_all('pre', attrs={'data-type': 'code'}):
        try:
            language = code_tag.attrs['data-code-language']
        except KeyError:
            raise SystemExit(_('No “data-code-language” attribute specified for code highlight area.'))
        else:
            lexer = get_lexer_by_name(language)

        indent = int(code_tag.attrs.get('data-code-indent', '0'))
        lines = [line[indent:] for line in code_tag.text.splitlines()]
        content = '\n'.join(lines)

        formatter = get_html_formatter()
        html = highlight(content, lexer, formatter)

        code_tag.replace_with(DontEscapeDammit(html))

    return soup
