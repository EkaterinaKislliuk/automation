import pytest
from BinaryMinHeap import MinHeap


@pytest.fixture
def heap():
    return MinHeap()


@pytest.mark.parametrize(
    "index,expected",
    [
        (1, 0),
        (2, 0),
        (3, 1),
        (4, 1),
        (5, 2),
    ],
)
def test_parent_typical_indices(heap, index, expected):
    assert heap._parent(index) == expected


@pytest.mark.parametrize("index,expected", [(0, -1)])
def test_parent_root_and_zero_index(heap, index, expected):
    assert heap._parent(index) == expected


@pytest.mark.parametrize("index,expected", [(-1, -1), (-2, -2)])
def test_parent_negative_indices(heap, index, expected):
    assert heap._parent(index) == expected


@pytest.mark.parametrize("index,expected", [(100, 49), (101, 50)])
def test_parent_large_indices(heap, index, expected):
    assert heap._parent(index) == expected


@pytest.mark.parametrize(
    "index,expected",
    list(enumerate([-1, 0, 0, 1, 1, 2, 2, 3, 3, 4])),
)
def test_parent_consecutive_indices(heap, index, expected):
    assert heap._parent(index) == expected