import pytest

from engine.tests.conftest import PROCESSOR_CLASSES


@pytest.fixture(params=PROCESSOR_CLASSES)
def model(request):
    return request.param
