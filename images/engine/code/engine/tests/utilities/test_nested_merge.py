import pytest

from engine.utilities import nested_merge


@pytest.mark.parametrize(
    'first, second, result',
    [
        [{}, {}, {}],
        [{1: 2}, {3: 4}, {1: 2, 3: 4}],
        [{1: 2}, {1: 3}, {1: 3}],
        [{1: {}}, {1: 2}, {1: 2}],
        [{1: 2}, {1: {}}, {1: {}}],
        [{1: {2: 3}}, {1: {4: 5}}, {1: {2: 3, 4: 5}}],
        [{1: {2: {3: 4}}}, {1: {2: {5: 6}}}, {1: {2: {3: 4, 5: 6}}}],
    ]
)
def test_nested_merge(first, second, result):
    nested_merge(first, second)
    assert first == result
