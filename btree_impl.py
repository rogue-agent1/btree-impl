#!/usr/bin/env python3
"""B-tree implementation for database indexing."""

class BTreeNode:
    def __init__(self, t, leaf=True):
        self.t = t
        self.leaf = leaf
        self.keys = []
        self.children = []

class BTree:
    def __init__(self, t=3):
        self.t = t
        self.root = BTreeNode(t)

    def search(self, key, node=None):
        node = node or self.root
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if i < len(node.keys) and node.keys[i] == key:
            return True
        if node.leaf:
            return False
        return self.search(key, node.children[i])

    def insert(self, key):
        root = self.root
        if len(root.keys) == 2 * self.t - 1:
            new_root = BTreeNode(self.t, False)
            new_root.children.append(self.root)
            self._split(new_root, 0)
            self.root = new_root
        self._insert_non_full(self.root, key)

    def _insert_non_full(self, node, key):
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(None)
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = key
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == 2 * self.t - 1:
                self._split(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], key)

    def _split(self, parent, i):
        t = self.t
        child = parent.children[i]
        new = BTreeNode(t, child.leaf)
        parent.keys.insert(i, child.keys[t - 1])
        parent.children.insert(i + 1, new)
        new.keys = child.keys[t:]
        child.keys = child.keys[:t - 1]
        if not child.leaf:
            new.children = child.children[t:]
            child.children = child.children[:t]

    def inorder(self, node=None):
        node = node or self.root
        result = []
        for i in range(len(node.keys)):
            if not node.leaf:
                result.extend(self.inorder(node.children[i]))
            result.append(node.keys[i])
        if not node.leaf:
            result.extend(self.inorder(node.children[-1]))
        return result

def test():
    bt = BTree(2)
    for v in [10, 20, 5, 6, 12, 30, 7, 17]:
        bt.insert(v)
    assert bt.search(6)
    assert bt.search(17)
    assert not bt.search(99)
    assert bt.inorder() == sorted([10, 20, 5, 6, 12, 30, 7, 17])
    # Large insert
    bt2 = BTree(3)
    for i in range(100):
        bt2.insert(i)
    assert bt2.inorder() == list(range(100))
    for i in range(100):
        assert bt2.search(i)
    assert not bt2.search(100)
    print("  btree_impl: ALL TESTS PASSED")

if __name__ == "__main__":
    test()
