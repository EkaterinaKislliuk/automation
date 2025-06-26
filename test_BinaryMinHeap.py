import pytest
from BinaryMinHeap import MinHeap

# Test: _parent returns correct parent index for various child indices
def test_parent_typical_indices():
    heap = MinHeap()
    # For index 1, parent is 0
    assert heap._parent(1) == 0
    # For index 2, parent is 0
    assert heap._parent(2) == 0
    # For index 3, parent is 1
    assert heap._parent(3) == 1
    # For index 4, parent is 1
    assert heap._parent(4) == 1
    # For index 5, parent is 2
    assert heap._parent(5) == 2

# Test: _parent for root index (should return -1)
def test_parent_root_index():
    heap = MinHeap()
    assert heap._parent(0) == -1

# Test: _parent for negative index (edge case)
def test_parent_negative_index():
    heap = MinHeap()
    # For index -1, parent is -1
    assert heap._parent(-1) == -1
    # For index -2, parent is -2
    assert heap._parent(-2) == -2

# Test: _parent for large index
def test_parent_large_index():
    heap = MinHeap()
    assert heap._parent(100) == 49
    assert heap._parent(101) == 50


# Test: _parent for zero index (should always be -1)
def test_parent_zero_index():
    heap = MinHeap()
    assert heap._parent(0) == -1

# Test: _parent for consecutive indices to check pattern
def test_parent_consecutive_indices():
    heap = MinHeap()
    results = [heap._parent(i) for i in range(10)]
    expected = [-1, 0, 0, 1, 1, 2, 2, 3, 3, 4]
    assert results == expected



if __name__ == "__main__":
    test_parent_typical_indices()
    test_parent_root_index()
    test_parent_negative_index()
    test_parent_large_index()
    test_parent_zero_index()
    test_parent_consecutive_indices()