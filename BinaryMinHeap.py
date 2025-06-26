import random
import json

class MinHeap:
    """
    Binary Min Heap implementation.
    Supports insert, extract_min, peek_min, heapify, decrease_key, and delete operations.
    """

    def __init__(self):
        """Initialize an empty min heap."""
        self.heap = []

    def _parent(self, index):
        return (index - 1) // 2

    def _left(self, index):
        return 2 * index + 1

    def _right(self, index):
        return 2 * index + 2

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def insert(self, key):
        """Insert a new key into the heap."""
        self.heap.append(key)
        self._sift_up(len(self.heap) - 1)

    def _sift_up(self, index):
        while index > 0 and self.heap[self._parent(index)] > self.heap[index]:
            self._swap(index, self._parent(index))
            index = self._parent(index)

    def extract_min(self):
        """Remove and return the minimum element from the heap."""
        if not self.heap:
            raise IndexError("extract_min from empty heap")
        min_elem = self.heap[0]
        last_elem = self.heap.pop()
        if self.heap:
            self.heap[0] = last_elem
            self._sift_down(0)
        return min_elem

    def _sift_down(self, index):
        size = len(self.heap)
        while True:
            left = self._left(index)
            right = self._right(index)
            smallest = index

            if left < size and self.heap[left] < self.heap[smallest]:
                smallest = left
            if right < size and self.heap[right] < self.heap[smallest]:
                smallest = right
            if smallest == index:
                break
            self._swap(index, smallest)
            index = smallest

    def peek_min(self):
        """Return the minimum element without removing it."""
        if not self.heap:
            raise IndexError("peek_min from empty heap")
        return self.heap[0]

    def heapify(self, iterable):
        """Build a heap from an iterable of elements."""
        self.heap = list(iterable)
        for i in reversed(range(len(self.heap) // 2)):
            self._sift_down(i)

    def decrease_key(self, index, new_key):
        """
        Decrease the value of the key at index to new_key.
        Assumes new_key is less than the current key.
        """
        if new_key > self.heap[index]:
            raise ValueError("new key is greater than current key")
        self.heap[index] = new_key
        self._sift_up(index)

    def delete(self, index):
        """Delete the element at the specified index."""
        if index >= len(self.heap):
            raise IndexError("index out of range")
        self.decrease_key(index, float('-inf'))
        self.extract_min()

    def __len__(self):
        """Return the number of elements in the heap."""
        return len(self.heap)

    def __bool__(self):
        """Return True if the heap is not empty."""
        return bool(self.heap)

    def __repr__(self):
        return f"MinHeap({self.heap})"

def main():
    # Option 1: Generate random data
    data = [random.randint(1, 100) for _ in range(15)]
    print("Generated data:", data)

    # Option 2: Load data from a JSON file (uncomment to use)
    # with open('heap_data.json', 'r') as f:
    #     data = json.load(f)
    # print("Loaded data from JSON:", data)

    # Populate the heap
    heap = MinHeap()
    heap.heapify(data)
    print("Heap after heapify:", heap)

    # Demonstrate heap operations
    print("Extract min:", heap.extract_min())
    print("Heap after extract_min:", heap)
    heap.insert(42)
    print("Heap after insert(42):", heap)
    print("Peek min:", heap.peek_min())

if __name__ == "__main__":
    main()