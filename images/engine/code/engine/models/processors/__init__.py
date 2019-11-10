from engine.models.processors.wrapper import Wrapper
from engine.models.processors.brotler import Brotler
from engine.models.processors.minifier import Minifier
from engine.models.processors.typograph import Typograph
from engine.models.processors.hyphenator import Hyphenator
from engine.models.processors.hanginator import Hanginator
from engine.models.processors.highlighter import Highlighter

PROCESSORS = {
    'wrapper': Wrapper,
    'brotler': Brotler,
    'minifier': Minifier,
    'typograph': Typograph,
    'hyphenator': Hyphenator,
    'hanginator': Hanginator,
    'highlighter': Highlighter,
}
