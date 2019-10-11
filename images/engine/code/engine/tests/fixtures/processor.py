import pytest

from engine.models.processor import Processor


@pytest.fixture
def processor():
    return Processor
