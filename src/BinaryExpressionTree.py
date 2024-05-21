class Node:
    def __init__(self, value) -> None:
        self.value = value
        self.left = None
        self.right = None


class BinaryExpressionTree:
    def __init__(self):
        self.root = None

    @staticmethod
    def syntax_error(expression: str) -> bool:
        """This method is used to check whether the expression is correct or not."""
        i, j, k = 0, 0, 0
        for char in expression:
            if char == "(":
                i += 1
            elif char == ")":
                j += 1
            elif expression[k] not in "0123456789" and expression[k+1] not in "0123456789":
                if expression[k] in "+-*/" and expression[k+1] == "(":
                    continue
                else:
                    print("Missing operand between operators")
                    return False
            k += 1
        if i != j:
            print("Unbalanced parentheses")
            return False

        return True

    def insert(self, root: Node, child: Node, direction="left") -> None:
        """This method inserts child node into the binary tree, you can specify the direction."""
        if root is None:
            self.root = child
            return
        elif root.left is None:
            root.left = child
            return
        elif root.right is None:
            root.right = child
            return
        if direction == "left":
            return self.insert(root.left, child)
        return self.insert(root.right, child, direction="right")

    def print(self, node, prefix="", is_left=True):
        if not node:
            print("Empty Tree")
            return
        if node.right:
            self.print(node.right, prefix + ("│   " if is_left else "    "), False)
        print(prefix + ("└── " if is_left else "┌── ") + str(node.value))
        if node.left:
            self.print(node.left, prefix + ("    " if is_left else "│   "), True)

    def set_tree(self, expression: str, checked=False):
        if expression == "":
            return
        expression = expression.replace(" ", "")  # Any whitespace is removed
        if not checked:  # To just check once the expression
            if self.syntax_error(expression):
                checked = True
        i = len(expression) // 2
        while i >= 0:
            if expression[i] in "+-*/":
                self.root = Node(expression[i])
                break
            i -= 1
        i = 0
        visited_positions = []  # This list saves all the positions that already have been used
        for char in expression:
            if char == self.root.value:  # If we're on the root previously set, don't do anything
                i += 1
                continue
            if char == "(" and i not in visited_positions:  # First insert the operation between parentheses
                operation = Node(expression[i+2])
                operation.left = Node(expression[i+1])
                operation.right = Node(expression[i+3])
                visited_positions.append(i), visited_positions.append(i+1), visited_positions.append(i+2), visited_positions.append(i+3)
                self.insert(tree.root, operation)
            elif char in "+-*/" and i not in visited_positions:
                operation = Node(expression[i])
                operation.left = Node(expression[i - 1])
                if expression[i + 1] == "(":  # This checks if the next character of an operation is a parenthesis
                    sub_operation = Node(expression[i + 3])
                    sub_operation.left = Node(expression[i + 2])  # Create a node with the operation between the parentheses
                    sub_operation.right = Node(expression[i + 4])
                    visited_positions.append(i), visited_positions.append(i+1), visited_positions.append(i+2)
                    visited_positions.append(i+3), visited_positions.append(i+4)  # Inserts all the visited positions
                    operation.right = sub_operation
                else:  # If it's not a parenthesis, just add the number to the right child
                    operation.right = Node(expression[i+1])
                if i >= len(expression) // 2:  # This conditional checks whether the position is above the middle of the expression
                    # If it's above put the node at the right of the tree
                    self.insert(tree.root, operation, direction="right")
                else:
                    # Else, put it in the left (default value of direction is "left")
                    self.insert(tree.root, operation)
            i += 1

    def evaluate_tree(self):
        if self.root is None:
            return



tree = BinaryExpressionTree()
tree.set_tree("(5 + 4) * 3 / (4 + 2)")
tree.print(tree.root)
