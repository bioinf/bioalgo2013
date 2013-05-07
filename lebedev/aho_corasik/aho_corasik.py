# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
from collections import deque


class Node(object):
    def __init__(self, children=None, parent=None, parent_ch=None,
                 suffix_link=None, go=None, is_leaf=False):
        self.children = children or {}
        self.parent = parent
        self.parent_ch = parent_ch
        self.suffix_link = suffix_link
        self.go = go or {}
        self.is_leaf = is_leaf


class Trie(object):
    def __init__(self):
        self.nodes = [Node()]  # Add root.

    def _link(self, i):
        current = self.nodes[i]
        if current.suffix_link is None:
            if not i or current.parent == 0:
                current.suffix_link = 0
            else:
                current.suffix_link = self._go(
                    self._link(current.parent), current.parent_ch)

        return current.suffix_link

    def _go(self, i, ch):
        current = self.nodes[i]
        if ch not in current.go:
            if ch in current.children:
                current.go[ch] = current.children[ch]
            elif not i:
                current.go[ch] = 0
            else:
                current.go[ch] = self._go(self._link(i), ch)

        return current.go[ch]

    def walk(self, f):
        q = deque([0])
        while q:
            i = q.popleft()
            current = self.nodes[i]
            if current.parent != i:
                f(i, current)  # Skip root.
            q.extend(current.children.values())

    def dump(self, path):
        with open(path, "w") as f:
            f.write("digraph trie {\n")
            self.walk(lambda i, current:
                      f.write("{0.parent} -> {1} [label={0.parent_ch}]\n"
                              .format(current, i)))
            self.walk(lambda i, current:
                      f.write("{0} -> {1} [style=dotted,color=blue]\n"
                              .format(i, self._link(i))))
            f.write("}\n")

    def add(self, s):
        i = 0
        for ch in s:
            current = self.nodes[i]
            if ch not in current.children:
                self.nodes.append(Node(parent=i, parent_ch=ch))
                current.children[ch] = len(self) - 1

            i = current.children[ch]

        if s:
            current.is_leaf = True

    def __iter__(self):
        return iter(self.nodes)

    def __len__(self):
        return len(self.nodes)


def trie(*seqs):
    t = Trie()
    for seq in seqs:
        t.add(seq)

    t.walk(lambda i, current:
           print(current.parent + 1, i + 1, current.parent_ch))


def atrie(*seqs):
    t = Trie()
    for seq in seqs:
        t.add(seq)

    t.walk(lambda i, current:
           print(current.parent + 1, i + 1, current.parent_ch))
    t.walk(lambda i, current: print(i + 1, t._link(i) + 1, "S"))
