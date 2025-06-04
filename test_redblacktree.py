import unittest
from RedBlackTree import RedBlackTree, Color, RBNode

class TestRedBlackTree(unittest.TestCase):
    def setUp(self):
        """Set up a new tree before each test"""
        self.tree = RedBlackTree()

    def test_init(self):
        """Test initialization of Red-Black tree"""
        self.assertEqual(self.tree.root, self.tree.NIL)
        self.assertEqual(self.tree.NIL.color, Color.BLACK)
        self.assertIsNone(self.tree.NIL.key)

    def test_insert_single(self):
        """Test inserting a single node"""
        self.tree.insert(10)
        self.assertEqual(self.tree.root.key, 10)
        self.assertEqual(self.tree.root.color, Color.BLACK)
        self.assertEqual(self.tree.root.left, self.tree.NIL)
        self.assertEqual(self.tree.root.right, self.tree.NIL)

    def test_insert_multiple(self):
        """Test inserting multiple nodes"""
        keys = [10, 20, 5, 15, 25]
        for key in keys:
            self.tree.insert(key)

        # Verify root properties
        self.assertEqual(self.tree.root.key, 10)
        self.assertEqual(self.tree.root.color, Color.BLACK)

        # Verify tree structure
        self.assertEqual(self.tree.root.right.key, 20)
        self.assertEqual(self.tree.root.left.key, 5)

    def test_insert_none(self):
        """Test inserting None value"""
        with self.assertRaises(ValueError):
            self.tree.insert(None)

    def test_delete_single(self):
        """Test deleting a single node"""
        self.tree.insert(10)
        self.tree.delete(10)
        self.assertEqual(self.tree.root, self.tree.NIL)

    def test_delete_multiple(self):
        """Test deleting multiple nodes"""
        keys = [10, 20, 5, 15, 25]
        for key in keys:
            self.tree.insert(key)

        self.tree.delete(20)
        self.assertIsNone(self._find_key(self.tree.root, 20))

    def test_delete_nonexistent(self):
        """Test deleting a non-existent key"""
        self.tree.insert(10)
        self.tree.delete(20)  # Should not raise any error
        self.assertEqual(self.tree.root.key, 10)

    def test_find_node(self):
        """Test finding nodes"""
        keys = [10, 20, 5]
        for key in keys:
            self.tree.insert(key)

        node = self.tree._find_node(20)
        self.assertEqual(node.key, 20)
        
        node = self.tree._find_node(99)
        self.assertIsNone(node)

    def test_inorder_traversal(self):
        """Test inorder traversal"""
        keys = [10, 20, 5, 15, 25]
        for key in keys:
            self.tree.insert(key)

        traversal = [k for k, _ in self.tree.inorder_traversal()]
        self.assertEqual(traversal, sorted(keys))

    def test_tree_properties(self):
        """Test Red-Black tree properties"""
        keys = [10, 20, 5, 15, 25, 30, 35]
        for key in keys:
            self.tree.insert(key)

        self.assertTrue(self._is_valid_rb_tree(self.tree.root))

    def test_rotations(self):
        """Test left and right rotations"""
        self.tree.insert(30)
        self.tree.insert(20)
        self.tree.insert(40)
        
        # Force a left rotation
        old_root = self.tree.root
        self.tree._left_rotate(old_root)
        self.assertNotEqual(self.tree.root, old_root)

    def _is_valid_rb_tree(self, node):
        """Helper method to verify Red-Black tree properties"""
        if node == self.tree.NIL:
            return True

        # Property 1: Root is black
        if node == self.tree.root:
            if node.color != Color.BLACK:
                return False

        # Property 2: No two adjacent red nodes
        if node.color == Color.RED:
            if (node.left != self.tree.NIL and node.left.color == Color.RED) or \
               (node.right != self.tree.NIL and node.right.color == Color.RED):
                return False

        # Recursively check children
        return self._is_valid_rb_tree(node.left) and self._is_valid_rb_tree(node.right)

    def _find_key(self, node, key):
        """Helper method to find a key in the tree"""
        if node == self.tree.NIL:
            return None
        if node.key == key:
            return node
        if key < node.key:
            return self._find_key(node.left, key)
        return self._find_key(node.right, key)

    def test_insert_duplicate(self):
        """Test inserting duplicate keys (should not add duplicates)"""
        self.tree.insert(10)
        self.tree.insert(10)
        traversal =  [k for k, _ in self.tree.inorder_traversal()]
        self.assertEqual(traversal.count(10), 1)

    def test_bulk_insert_and_delete(self):
        """Test inserting and deleting a large number of nodes"""
        keys = list(range(1000))
        for key in keys:
            self.tree.insert(key)
        for key in keys:
            self.tree.delete(key)
        self.assertEqual(self.tree.root, self.tree.NIL)

    def test_delete_root(self):
        """Test deleting the root node repeatedly"""
        keys = [50, 30, 70, 20, 40, 60, 80]
        for key in keys:
            self.tree.insert(key)
        while self.tree.root != self.tree.NIL:
            root_key = self.tree.root.key
            self.tree.delete(root_key)
        self.assertEqual(self.tree.root, self.tree.NIL)

    def test_left_right_heavy_tree(self):
        """Test tree balancing with left-heavy and right-heavy insertions"""
        # Left-heavy
        for key in reversed(range(10)):
            self.tree.insert(key)
        self.assertTrue(self._is_valid_rb_tree(self.tree.root))
        # Right-heavy
        self.tree = RedBlackTree()
        for key in range(10):
            self.tree.insert(key)
        self.assertTrue(self._is_valid_rb_tree(self.tree.root))

    def test_draw_tree_output(self):
        """Test that draw_tree runs without error on a populated tree"""
        keys = [10, 20, 5, 15, 25]
        for key in keys:
            self.tree.insert(key)
        # Should not raise any exceptions
        self.tree.draw_tree()

    def test_inorder_after_deletion(self):
        """Test inorder traversal after deletions"""
        keys = [10, 20, 5, 15, 25]
        for key in keys:
            self.tree.insert(key)
        self.tree.delete(20)
        traversal = [k for k, _ in self.tree.inorder_traversal()]
        self.assertNotIn(20, traversal)
        self.assertEqual(sorted(traversal), [5, 10, 15, 25])

def run_tests():
    """Run the unit tests"""
    unittest.main()

if __name__ == '__main__':
    run_tests()