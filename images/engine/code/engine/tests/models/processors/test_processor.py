import pytest

from engine.tests.conftest import PROCESSOR_CLASSES


@pytest.fixture(params=PROCESSOR_CLASSES)
def model(request):
    return request.param


@pytest.mark.parametrize('method', ['process_content', 'process_file', 'get_file_path', 'IS_BINARY'])
def test_classes_share_interface(model, method):
    assert hasattr(model, method)
