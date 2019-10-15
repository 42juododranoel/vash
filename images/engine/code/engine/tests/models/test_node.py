import pytest

from engine.tests.conftest import NODE_SUBCLASSES

# TODO: refactor to split abstract base methods and normal methods

# TODO: test _get_absolute_path
# TODO: test __init__
# TODO: test path
# TODO: test move to the same folder
# TODO: test move to upper folder
# TODO: test move to lower folder ← hard
# TODO: test move idles when missing


@pytest.mark.parametrize('model', NODE_SUBCLASSES)
def test_is_present_true_when_created(create, model, node_path):
    node = create(model, node_path)
    assert node.is_present


@pytest.mark.parametrize('model', NODE_SUBCLASSES)
def test_is_present_false_when_not_created(model, node_path):
    node = model(node_path)
    assert not node.is_present


@pytest.mark.parametrize('model', NODE_SUBCLASSES)
def test_create_idles_when_created(create, model, node_path):
    node = create(model, node_path)
    assert node.is_present
    node.create()


@pytest.mark.parametrize('model', NODE_SUBCLASSES)
def test_create_creates_when_not_created(model, node_path):
    node = model(node_path)
    assert not node.is_present
    node.create()
    assert node.is_present


@pytest.mark.parametrize('model', NODE_SUBCLASSES)
def test_delete_deletes_when_created(create, model, node_path):
    node = create(model, node_path)
    assert node.is_present
    node.delete()
    assert not node.is_present


@pytest.mark.parametrize('model', NODE_SUBCLASSES)
def test_delete_idles_when_not_created(model, node_path):
    node = model(node_path)
    assert not node.is_present
    node.delete()


# TODO: broken by global teardown
# @pytest.mark.parametrize('model', NODE_SUBCLASSES)
# def test_move_moves_when_created(create, model, node_path, node_new_path):
#     node = create(model, node_path)
#     node.move(node_new_path)
#     assert node.is_present
