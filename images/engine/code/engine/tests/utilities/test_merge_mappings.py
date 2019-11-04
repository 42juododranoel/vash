import pytest

from engine.utilities import merge_mappings


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
def test_merge_mappings(first, second, result):
    assert result == merge_mappings(first, second)


def test_modifies_first_argument():
    first = {}
    second = {1: 2}
    merge_mappings(first, second)
    assert first == second
