#!/usr/bin/env python3
"""B-Tree implementation — zero-dep."""

class BTreeNode:
    def __init__(self, leaf=True):
        self.keys=[]; self.children=[]; self.leaf=leaf

class BTree:
    def __init__(self, t=3):
        self.root=BTreeNode(); self.t=t
    def search(self, key, node=None):
        node=node or self.root; i=0
        while i<len(node.keys) and key>node.keys[i]: i+=1
        if i<len(node.keys) and key==node.keys[i]: return (node,i)
        if node.leaf: return None
        return self.search(key,node.children[i])
    def insert(self, key):
        r=self.root
        if len(r.keys)==2*self.t-1:
            s=BTreeNode(leaf=False); s.children=[r]; self._split(s,0); self.root=s
        self._insert_nonfull(self.root,key)
    def _insert_nonfull(self, node, key):
        i=len(node.keys)-1
        if node.leaf:
            node.keys.append(None)
            while i>=0 and key<node.keys[i]: node.keys[i+1]=node.keys[i]; i-=1
            node.keys[i+1]=key
        else:
            while i>=0 and key<node.keys[i]: i-=1
            i+=1
            if len(node.children[i].keys)==2*self.t-1:
                self._split(node,i)
                if key>node.keys[i]: i+=1
            self._insert_nonfull(node.children[i],key)
    def _split(self, parent, i):
        t=self.t; child=parent.children[i]
        new=BTreeNode(leaf=child.leaf)
        parent.keys.insert(i,child.keys[t-1])
        parent.children.insert(i+1,new)
        new.keys=child.keys[t:]; child.keys=child.keys[:t-1]
        if not child.leaf:
            new.children=child.children[t:]; child.children=child.children[:t]
    def traverse(self, node=None):
        node=node or self.root; result=[]
        for i in range(len(node.keys)):
            if not node.leaf: result.extend(self.traverse(node.children[i]))
            result.append(node.keys[i])
        if not node.leaf: result.extend(self.traverse(node.children[-1]))
        return result

if __name__=="__main__":
    bt=BTree(t=3)
    for k in [10,20,5,6,12,30,7,17,3,1,15,25,35,40,50]:
        bt.insert(k)
    print(f"Traversal: {bt.traverse()}")
    print(f"Root keys: {bt.root.keys}")
    for k in [6,15,50,99]:
        r=bt.search(k)
        print(f"  Search {k}: {'found' if r else 'not found'}")
