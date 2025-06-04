from enum import Enum

class Color(Enum):
    """Enum for node colors in Red-Black tree"""
    RED = 1
    BLACK = 2

class RBNode:
    """Node class for Red-Black tree"""
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None
        self.color = Color.RED  # New nodes are always red
        
class RedBlackTree:
    """
    Red-Black Tree implementation with self-balancing properties.
    Properties:
    1. Every node is either red or black
    2. Root is always black
    3. No two adjacent red nodes (red node cannot have red parent or red child)
    4. Every path from root to leaf has same number of black nodes
    """
    
    def __init__(self):
        """Initialize empty Red-Black tree"""
        self.NIL = RBNode(None)  # Sentinel node
        self.NIL.color = Color.BLACK
        self.root = self.NIL

    def insert(self, key):
        """Insert a new key into the Red-Black tree"""
        if key is None:
            raise ValueError("Cannot insert None as a key")
          # Check for duplicate key before insertion
        if self._find_node(key) is not None:
            # Duplicate key found, do not insert
            return


        node = RBNode(key)
        node.left = self.NIL
        node.right = self.NIL
        
        # Do standard BST insert
        y = None
        x = self.root
        
        while x != self.NIL:
            y = x
            if node.key < x.key:
                x = x.left
            else:
                x = x.right
        
        node.parent = y
        if y == None:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node
            
        # Fix Red-Black tree properties
        self._fix_insert(node)

    def _fix_insert(self, node):
        """Fix Red-Black tree properties after insertion"""
        while node.parent and node.parent.color == Color.RED:
            if node.parent == node.parent.parent.left:
                y = node.parent.parent.right
                if y.color == Color.RED:
                    node.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self._left_rotate(node)
                    node.parent.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    self._right_rotate(node.parent.parent)
            else:
                y = node.parent.parent.left
                if y.color == Color.RED:
                    node.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._right_rotate(node)
                    node.parent.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    self._left_rotate(node.parent.parent)
                    
            if node == self.root:
                break
        self.root.color = Color.BLACK

    def delete(self, key):
        """Delete a key from the Red-Black tree"""
        z = self._find_node(key)
        if z:
            self._delete_node(z)

    def _delete_node(self, z):
        """Helper method to delete a node"""
        y = z
        y_original_color = y.color
        
        if z.left == self.NIL:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            y_original_color = y.color
            x = y.right
            
            if y.parent == z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
                
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
            
        if y_original_color == Color.BLACK:
            self._fix_delete(x)

    def _fix_delete(self, x):
        """Fix Red-Black tree properties after deletion"""
        while x != self.root and x.color == Color.BLACK:
            if x == x.parent.left:
                w = x.parent.right
                if w.color == Color.RED:
                    w.color = Color.BLACK
                    x.parent.color = Color.RED
                    self._left_rotate(x.parent)
                    w = x.parent.right
                    
                if w.left.color == Color.BLACK and w.right.color == Color.BLACK:
                    w.color = Color.RED
                    x = x.parent
                else:
                    if w.right.color == Color.BLACK:
                        w.left.color = Color.BLACK
                        w.color = Color.RED
                        self._right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = Color.BLACK
                    w.right.color = Color.BLACK
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == Color.RED:
                    w.color = Color.BLACK
                    x.parent.color = Color.RED
                    self._right_rotate(x.parent)
                    w = x.parent.left
                    
                if w.right.color == Color.BLACK and w.left.color == Color.BLACK:
                    w.color = Color.RED
                    x = x.parent
                else:
                    if w.left.color == Color.BLACK:
                        w.right.color = Color.BLACK
                        w.color = Color.RED
                        self._left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = Color.BLACK
                    w.left.color = Color.BLACK
                    self._right_rotate(x.parent)
                    x = self.root
        x.color = Color.BLACK

    def _left_rotate(self, x):
        """Perform left rotation"""
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, x):
        """Perform right rotation"""
        y = x.left
        x.left = y.right
        if y.right != self.NIL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def _find_node(self, key):
        """Find node with given key"""
        node = self.root
        while node != self.NIL:
            if key == node.key:
                return node
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return None

    def _minimum(self, node):
        """Find minimum key in subtree"""
        while node.left != self.NIL:
            node = node.left
        return node

    def _transplant(self, u, v):
        """Replace subtree rooted at u with subtree rooted at v"""
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def inorder_traversal(self):
        """Perform inorder traversal"""
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        """Helper method for inorder traversal"""
        if node != self.NIL:
            self._inorder_recursive(node.left, result)
            result.append((node.key, node.color))
            self._inorder_recursive(node.right, result)

    def draw_tree(self):
        """Visualize the Red-Black tree structure"""
        def _get_tree_lines(node, level=0, prefix="Root: "):
            if node == self.NIL:
                return []
            
            lines = []
            color = "R" if node.color == Color.RED else "B"
            lines.append(f"{' ' * (level * 4)}{prefix}{node.key} ({color})")
            
            if node.left != self.NIL or node.right != self.NIL:
                if node.left != self.NIL:
                    lines.extend(_get_tree_lines(node.left, level + 1, "L── "))
                else:
                    lines.append(f"{' ' * ((level + 1) * 4)}L── NIL (B)")
                    
                if node.right != self.NIL:
                    lines.extend(_get_tree_lines(node.right, level + 1, "R── "))
                else:
                    lines.append(f"{' ' * ((level + 1) * 4)}R── NIL (B)")
                    
            return lines

        if self.root == self.NIL:
            print("Empty tree")
            return

        print("\nRed-Black Tree Structure:")
        print("-" * 50)
        tree_lines = _get_tree_lines(self.root)
        print("\n".join(tree_lines))
        print("-" * 50)

def main():
    """Test Red-Black tree operations"""
    from random import uniform, randint
    
    # Create tree and insert random values
    rb_tree = RedBlackTree()
    num_nodes = randint(15, 55)
    random_keys = [round(uniform(-100.0, 100.0), 2) for _ in range(num_nodes)]
    
    print(f"Inserting {num_nodes} random keys:")
    print(f"Input values: {random_keys}")
    
    for key in random_keys:
        rb_tree.insert(key)
    
    # Display tree
    rb_tree.draw_tree()
    
    # Demonstrate traversal
    print("\nInorder traversal (key, color):")
    print(rb_tree.inorder_traversal())
    
    # Demonstrate deletion
    delete_key = random_keys[randint(0, len(random_keys)-1)]
    print(f"\nDeleting key {delete_key}")
    rb_tree.delete(delete_key)
    
    print("\nTree after deletion:")
    rb_tree.draw_tree()

if __name__ == "__main__":
    main()