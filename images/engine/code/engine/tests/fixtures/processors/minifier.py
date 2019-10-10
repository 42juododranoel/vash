import pytest

from engine.models.processors.minifier import Minifier


@pytest.fixture
def minifier():
    minifier = Minifier()
    return minifier
