from constance import config
from richtypo import Richtypo


class RichtypoWhichBypassesStyleTag(Richtypo):
    bypass_tags = Richtypo.bypass_tags + ['style']


def typograph_html(html):
    ruleset = config.SITE_LANGUAGE + '-lite'
    richtypo = RichtypoWhichBypassesStyleTag(ruleset)
    return richtypo.richtypo(html)
