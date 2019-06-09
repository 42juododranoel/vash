from pygments import styles
from pygments.formatters.html import HtmlFormatter


def get_html_formatter():
    style = styles.get_style_by_name('default')
    formatter = HtmlFormatter(
        style=style,
        linenos='inline',
        classprefix='code-',
    )
    return formatter
