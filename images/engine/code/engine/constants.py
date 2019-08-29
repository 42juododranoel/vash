import gettext

_ = gettext.gettext

FILES_URL = '/files'

FILES_FOLDER = '/resources/files'
PAGES_FOLDER = '/resources/pages'
TEMPLATES_FOLDER = '/resources/templates'

RENDERED_HTML_FOLDER = f'{PAGES_FOLDER}/_html'
RENDERED_JSON_FOLDER = f'{PAGES_FOLDER}/_json'

TAGS_TO_WRAP = ['p', 'h1', 'h2', 'h3', 'figcaption', 'ul']
CLASSES_TO_WRAP = ['title', 'subscription', 'accent', 'before-list', 'before-indent', 'indent-after']

SLUG_HELP_TEXT = _('0-9, a-z, A-Z, -, _.')
REQUIRED_BLOCKS = ['meta', 'styles', 'body']

FRONTEND_BREAKPOINT_SM = 0
FRONTEND_BREAKPOINT_MD = 960
FRONTEND_BREAKPOINT_LG = 1400
FRONTEND_COLUMNS_COUNT = 16
