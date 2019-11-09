from engine.models.processors.wrapper import Wrapper
from engine.models.processors.brotler import Brotler
from engine.models.processors.minifier import Minifier
from engine.models.processors.typograph import Typograph

PROCESSORS = {
    'wrapper': Wrapper,
    'brotler': Brotler,
    'minifier': Minifier,
    'typograph': Typograph,
}
