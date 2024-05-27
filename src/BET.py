from class_node import Node as Node


class BinaryExpressionTree:
    def __init__(self):
        self.root = None

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

    @staticmethod
    def syntax_error(expression: str):
        """This method is used to check whether the expression is correct or not."""
        expression = expression.replace(" ", "")
        i, j, k = 0, 0, 0
        for char in expression:
            if char == "(":
                i += 1
            elif char == ")":
                j += 1
            elif expression[k].isalpha():
                print("Character not allowed")
                return False
            elif expression[k] not in "0123456789" and expression[k + 1] not in "0123456789":
                if expression[k] in "+-*/" and expression[k + 1] == "(":
                    k += 1
                    continue
                elif expression[k+1].isalpha():
                    print("Character not allowed")
                    return False
                else:
                    print("Missing operand between operators")
                    return False
            k += 1
        if i != j:
            print("Unbalanced parentheses")
            return False

        return expression

    def print(self, node: Node, prefix="", is_left=True):
        if not node:
            print("Empty Tree")
            return
        if node.right:
            self.print(node.right, prefix + ("│   " if is_left else "    "), False)
        print(prefix + ("└── " if is_left else "┌── ") + str(node.value))
        if node.left:
            self.print(node.left, prefix + ("    " if is_left else "│   "), True)

    def set_root(self, string: str, operands="+-", right_limit=0, left_limit=0):
        if not string:
            return
        if "+" not in string and "-" not in string and "*" not in string and "/" not in string:
            string = string.replace("(", "").replace(")", "")
            return int(string)
        right_limit = len(string) - 1
        if string[-1] == ")":
            for j in range(right_limit, 0, -1):
                if string[j] == "(":
                    right_limit = j
                    break
        for k in range(right_limit - 1, 0, -1):
            if string[k] == ")":
                left_limit = k
                break
        for i in range(right_limit - 1, left_limit, -1):
            if string[i] in operands:
                return i
        return self.set_root(string, "*/", right_limit, left_limit)

    def update_child(self, cur_node: Node, value, new_node: Node):
        if not cur_node:
            return
        if cur_node.value == value:
            cur_node.value = new_node.value
            cur_node.left = new_node.left
            cur_node.right = new_node.right
            return
        if cur_node.left:
            self.update_child(cur_node.left, value, new_node)
        self.update_child(cur_node.right, value, new_node)

    def set_tree(self, expression: str, node: Node):
        if not expression:
            return
        if (expression[0] == "(" and expression[1:].isdigit()) or (expression[:-1].isdigit() and expression[-1] == ")"):
            node.value = self.set_root(expression)
            return
        if not self.root:
            node = Node(expression[self.set_root(expression)])
            node.left = Node(expression[:self.set_root(expression)])
            node.right = Node(expression[self.set_root(expression) + 1:])
            self.insert(self.root, node)
        if not node.value.isdigit() and node is not self.root:
            node = Node(expression[self.set_root(expression)])
            node.left = Node(expression[:self.set_root(expression)])
            node.right = Node(expression[self.set_root(expression) + 1:])
            self.update_child(self.root, expression, node)
        if not node.left.value.isdigit():
            self.set_tree(expression[:self.set_root(expression)], node.left)
        if not node.right.value.isdigit():
            self.set_tree(expression[self.set_root(expression) + 1:], node.right)

    def evaluate_tree(self, cur_node: Node) -> float:
        if cur_node is None:
            return 0
        if str(cur_node.value).isdigit():
            return float(cur_node.value)
        if cur_node.value == "+":
            return self.evaluate_tree(cur_node.left) + self.evaluate_tree(cur_node.right)
        elif cur_node.value == "-":
            return self.evaluate_tree(cur_node.left) - self.evaluate_tree(cur_node.right)
        elif cur_node.value == "*":
            return self.evaluate_tree(cur_node.left) * self.evaluate_tree(cur_node.right)
        elif cur_node.value == "/":
            return self.evaluate_tree(cur_node.left) / self.evaluate_tree(cur_node.right)


# s="(5 + 4) * 3 / (4 + 2)"
# s="(4*3)-5*(6/2)"
# s="5+(9*2)-7"
# s="9*2-3/4"
# s="2+(4+2)"
tree = BinaryExpressionTree()
s = "5+3/2*(4+6)"
s = tree.syntax_error(s)
tree.set_tree(s, tree.root)
tree.print(tree.root)
print(tree.evaluate_tree(tree.root))
