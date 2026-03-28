#!/usr/bin/env python3
"""B-Tree implementation."""
import sys

class BTreeNode:
    def __init__(self, t, leaf=True):
        self.t = t; self.leaf = leaf; self.keys = []; self.children = []

class BTree:
    def __init__(self, t=3):
        self.t = t; self.root = BTreeNode(t)
    def search(self, key, node=None):
        if node is None: node = self.root
        i = 0
        while i < len(node.keys) and key > node.keys[i]: i += 1
        if i < len(node.keys) and key == node.keys[i]: return True
        if node.leaf: return False
        return self.search(key, node.children[i])
    def insert(self, key):
        r = self.root
        if len(r.keys) == 2*self.t - 1:
            s = BTreeNode(self.t, False); s.children.append(self.root)
            self._split(s, 0); self.root = s
        self._insert_nonfull(self.root, key)
    def _split(self, parent, i):
        t = self.t; y = parent.children[i]; z = BTreeNode(t, y.leaf)
        parent.keys.insert(i, y.keys[t-1])
        parent.children.insert(i+1, z)
        z.keys = y.keys[t:]; y.keys = y.keys[:t-1]
        if not y.leaf: z.children = y.children[t:]; y.children = y.children[:t]
    def _insert_nonfull(self, node, key):
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(0)
            while i >= 0 and key < node.keys[i]: node.keys[i+1] = node.keys[i]; i -= 1
            node.keys[i+1] = key
        else:
            while i >= 0 and key < node.keys[i]: i -= 1
            i += 1
            if len(node.children[i].keys) == 2*self.t - 1:
                self._split(node, i)
                if key > node.keys[i]: i += 1
            self._insert_nonfull(node.children[i], key)
    def inorder(self, node=None):
        if node is None: node = self.root
        result = []
        for i in range(len(node.keys)):
            if not node.leaf: result.extend(self.inorder(node.children[i]))
            result.append(node.keys[i])
        if not node.leaf: result.extend(self.inorder(node.children[-1]))
        return result

if __name__ == '__main__':
    import random
    t = BTree(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
    if '--demo' in sys.argv:
        nums = random.sample(range(1, 100), 20)
        for n in nums: t.insert(n)
        print(f"Inserted: {nums}")
        print(f"Sorted:   {t.inorder()}")
        print(f"Search 50: {t.search(50)}")
    else:
        print(f"B-Tree (t={t.t}). Commands: insert <n>, search <n>, list, quit")
        while True:
            try: line = input('> ').split()
            except EOFError: break
            if not line: continue
            if line[0] == 'quit': break
            elif line[0] == 'insert': t.insert(int(line[1])); print("OK")
            elif line[0] == 'search': print(t.search(int(line[1])))
            elif line[0] == 'list': print(t.inorder())
