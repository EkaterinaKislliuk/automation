from random import *
class AVLNode:
    """Node class for AVL tree"""
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    """
    AVL Tree implementation with self-balancing properties
    """
    
    def __init__(self):
        """Initialize an empty AVL tree"""
        self.root = None

    def height(self, node):
        """Get the height of a node"""
        if not node:
            return 0
        return node.height

    def balance_factor(self, node):
        """Calculate balance factor of a node"""
        if not node:
            return 0
        return self.height(node.left) - self.height(node.right)

    def update_height(self, node):
        """Update height of a node"""
        if not node:
            return
        node.height = max(self.height(node.left), self.height(node.right)) + 1

    def rotate_right(self, y):
        """Right rotation"""
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        self.update_height(y)
        self.update_height(x)

        return x

    def rotate_left(self, x):
        """Left rotation"""
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        self.update_height(x)
        self.update_height(y)

        return y

    def insert(self, key):
        """Insert a key into the AVL tree"""
        if key is None:
            raise ValueError("Cannot insert None as a key")
        self.root = self._insert_recursive(self.root, key)

    def _insert_recursive(self, node, key):
        """Helper method for recursive insertion"""
        # Perform standard BST insertion
        if key is None:
            raise ValueError("Cannot insert None as a key")
        if not node:
            return AVLNode(key)

        if key < node.key:
            node.left = self._insert_recursive(node.left, key)
        elif key > node.key:
            node.right = self._insert_recursive(node.right, key)
        else:
            return node  # Duplicate keys not allowed

        # Update height of current node
        self.update_height(node)

        # Get balance factor and balance if needed
        balance = self.balance_factor(node)

        # Left Left Case
        if balance > 1 and key < node.left.key:
            return self.rotate_right(node)

        # Right Right Case
        if balance < -1 and key > node.right.key:
            return self.rotate_left(node)

        # Left Right Case
        if balance > 1 and key > node.left.key:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        # Right Left Case
        if balance < -1 and key < node.right.key:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    def delete(self, key):
        """Delete a key from the AVL tree"""
        self.root = self._delete_recursive(self.root, key)

    def _delete_recursive(self, node, key):
        """Helper method for recursive deletion"""
        if not node:
            return node

        if key < node.key:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.key:
            node.right = self._delete_recursive(node.right, key)
        else:
            # Node with only one child or no child
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            # Node with two children
            temp = self._get_min_value_node(node.right)
            node.key = temp.key
            node.right = self._delete_recursive(node.right, temp.key)

        if not node:
            return node

        # Update height
        self.update_height(node)

        # Balance the tree
        balance = self.balance_factor(node)

        # Left Left Case
        if balance > 1 and self.balance_factor(node.left) >= 0:
            return self.rotate_right(node)

        # Left Right Case
        if balance > 1 and self.balance_factor(node.left) < 0:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        # Right Right Case
        if balance < -1 and self.balance_factor(node.right) <= 0:
            return self.rotate_left(node)

        # Right Left Case
        if balance < -1 and self.balance_factor(node.right) > 0:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    def _get_min_value_node(self, node):
        """Get node with minimum value in a subtree"""
        current = node
        while current.left:
            current = current.left
        return current

    def search(self, key):
        """Search for a key in the AVL tree"""
        return self._search_recursive(self.root, key)

    def _search_recursive(self, node, key):
        """Helper method for recursive search"""
        if not node or node.key == key:
            return node

        if key < node.key:
            return self._search_recursive(node.left, key)
        return self._search_recursive(node.right, key)

    def inorder_traversal(self):
        """Perform inorder traversal of the tree"""
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        """Helper method for recursive inorder traversal"""
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.key)
            self._inorder_recursive(node.right, result)

    def is_balanced(self):
        """Check if the tree is balanced"""
        return self._is_balanced_recursive(self.root)

    def _is_balanced_recursive(self, node):
        """Helper method for recursive balance checking"""
        if not node:
            return True

        balance = self.balance_factor(node)
        if abs(balance) > 1:
            return False

        return (self._is_balanced_recursive(node.left) and 
                self._is_balanced_recursive(node.right))

    def draw_tree(self):
        """
        Visualize the AVL tree structure using ASCII characters.
        """
        def _get_tree_lines(node, level=0, prefix="Root: "):
            if not node:
                return []
            
            lines = []
            
            # Add current node
            lines.append(" " * (level * 4) + prefix + str(round(node.key, 2)))
            
            # Process children
            if node.left or node.right:
                # Add left child
                if node.left:
                    lines.extend(_get_tree_lines(node.left, level + 1, "L── "))
                else:
                    lines.append(" " * ((level + 1) * 4) + "L── None")
                    
                # Add right child
                if node.right:
                    lines.extend(_get_tree_lines(node.right, level + 1, "R── "))
                else:
                    lines.append(" " * ((level + 1) * 4) + "R── None")
                    
            return lines

        if not self.root:
            print("Empty tree")
            return

        print("\nTree Structure:")
        print("-" * 50)
        tree_lines = _get_tree_lines(self.root)
        print("\n".join(tree_lines))
        print("-" * 50)
# ...existing code...

def main():
    """
    Main method to demonstrate AVL tree operations with random float values
    """
    
    
    # Generate list of random float values
    num_nodes = randint(15,55)  # Number of nodes to generate
    random_keys = [round(uniform(-100.0, 100.0), 2) for _ in range(num_nodes)]
    
    # Create and populate AVL tree
    avl_tree = AVLTree()
    
    
    print("Generating AVL tree with random float values:")
    print(f"Input values: {random_keys}")
    
    # Insert values into the tree
    for key in random_keys:
        avl_tree.insert(key)

    avl_tree.draw_tree()  
    # Verify tree properties
    print("\nTree properties:")
    print(f"Is balanced: {avl_tree.is_balanced()}")
    print(f"Inorder traversal: {avl_tree.inorder_traversal()}")
    
    # Demonstrate search
    search_key = random_keys[randint(0, len(random_keys)-1)]
    found_node = avl_tree.search(search_key)
    print(f"\nSearching for key {search_key}: {'Found' if found_node else 'Not found'}")
    
    # Demonstrate deletion
    delete_key = random_keys[randint(0, len(random_keys)-1)]
    print(f"\nDeleting key {delete_key}")
    avl_tree.delete(delete_key)
    print(f"Inorder traversal after deletion: {avl_tree.inorder_traversal()}")
    print(f"Tree remains balanced: {avl_tree.is_balanced()}")
    avl_tree.draw_tree()

if __name__ == "__main__":
    main()