#!/usr/bin/env python3
"""btree_impl - B-tree with insert, search, and display."""
import sys
class BTree:
    class Node:
        def __init__(self, leaf=True):
            self.keys=[]; self.children=[]; self.leaf=leaf
    def __init__(self, t=3):
        self.t=t; self.root=self.Node()
    def search(self, k, node=None):
        node=node or self.root; i=0
        while i<len(node.keys) and k>node.keys[i]: i+=1
        if i<len(node.keys) and k==node.keys[i]: return True
        if node.leaf: return False
        return self.search(k, node.children[i])
    def insert(self, k):
        r=self.root
        if len(r.keys)==2*self.t-1:
            s=self.Node(leaf=False); s.children.append(r)
            self._split(s,0); self.root=s
        self._insert_non_full(self.root, k)
    def _insert_non_full(self, x, k):
        i=len(x.keys)-1
        if x.leaf:
            x.keys.append(None)
            while i>=0 and k<x.keys[i]: x.keys[i+1]=x.keys[i]; i-=1
            x.keys[i+1]=k
        else:
            while i>=0 and k<x.keys[i]: i-=1
            i+=1
            if len(x.children[i].keys)==2*self.t-1:
                self._split(x,i)
                if k>x.keys[i]: i+=1
            self._insert_non_full(x.children[i], k)
    def _split(self, x, i):
        t=self.t; y=x.children[i]; z=self.Node(leaf=y.leaf)
        x.keys.insert(i, y.keys[t-1]); x.children.insert(i+1, z)
        z.keys=y.keys[t:]; y.keys=y.keys[:t-1]
        if not y.leaf: z.children=y.children[t:]; y.children=y.children[:t]
    def display(self, node=None, level=0):
        node=node or self.root
        print("  "*level+f"[{', '.join(map(str,node.keys))}]")
        for c in node.children: self.display(c, level+1)
if __name__=="__main__":
    bt=BTree(t=3)
    nums=[10,20,5,6,12,30,7,17,3,1,15,25,35,40]
    for x in nums: bt.insert(x)
    print(f"Inserted: {nums}"); bt.display()
    for x in [12,99]: print(f"Search {x}: {bt.search(x)}")
