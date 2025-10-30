class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
        self.size = 1 + (left.size if left else 0) + (right.size if right else 0)


def split(root, k):
    if root is None:
        return None, None

    left_size = root.left.size if root.left else 0

    if k <= left_size:
        # все k элементов в левом поддереве
        left, right = split(root.left, k)
        # создаем правое дерево с текущим корнем
        new_right = Node(root.value)
        new_right.right = root.right
        new_right.left = right
        new_right.size = 1 + (new_right.right.size if new_right.right else 0) + (new_right.left.size if new_right.left else 0)
        return left, new_right

    elif k == left_size + 1:
        # k элементов - это левое поддерево + корень
        left = Node(root.value)
        left.left = root.left
        left.size = 1 + (left.left.size if left.left else 0)

        return left, root.right

    else:
        # берем элементы из правого поддерева
        left, right = split(root.right, k - left_size - 1)
        # создаем левое дерево с текущим корнем
        new_left = Node(root.value)
        new_left.left = root.left
        new_left.right = left
        new_left.size = 1 + (new_left.left.size if new_left.left else 0) + (
            new_left.right.size if new_left.right else 0)
        return new_left, right


def build_node(nodes, idx):
    if idx == -1:
        return None
    value, left_idx, right_idx = nodes[idx]
    left_child = build_node(nodes, left_idx) if left_idx != -1 else None
    right_child = build_node(nodes, right_idx) if right_idx != -1 else None
    return Node(value, left_child, right_child)


def build_tree(n):
    nodes = [None] * (n + 1)
    for i in range(n):
        data = input().split()
        if len(data) < 4:
            print("Ошибка: нужно ввести 4 числа")
            break
        idx = int(data[0])
        value = int(data[1])
        left_idx = int(data[2])
        right_idx = int(data[3])
        nodes[idx] = (value, left_idx, right_idx)

    # находим корень (узел, к которому никто не привязан)
    referenced = set()
    for i in range(1, n + 1):
        if nodes[i]:
            _, left_idx, right_idx = nodes[i]
            if left_idx != -1:
                referenced.add(left_idx)
            if right_idx != -1:
                referenced.add(right_idx)

    for i in range(1, n + 1):
        if i not in referenced:
            return build_node(nodes, i)
    return None


def print_tree(node, level=0, prefix="Корень: "):
    if node is not None:
        print(" " * (level * 4) + prefix + f"{node.value} (размер: {node.size})")
        if node.left is not None or node.right is not None:
            if node.left:
                print_tree(node.left, level + 1, "L--- ")
            else:
                print(" " * ((level + 1) * 4) + "L--- None")
            if node.right:
                print_tree(node.right, level + 1, "R--- ")
            else:
                print(" " * ((level + 1) * 4) + "R--- None")


n = int(input())
root = build_tree(n)
k = int(input())
lbst, rbst = split(root, k)
print_tree(lbst)
print_tree(rbst)
