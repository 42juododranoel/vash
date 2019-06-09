from constance import config
from softhyphen.html import hyphenate


def hyphenate_html(html):
    return hyphenate(html, language='{0}-{0}'.format(config.SITE_LANGUAGE))
