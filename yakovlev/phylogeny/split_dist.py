import sys
import random
from StringIO import StringIO
from Bio import Phylo


class TreeNode(object):
    def __init__(self, node, parent=None):
        self.node = node
        self.in_edge = None
        self.parent = parent
        self.children = []
        if parent:
            parent.children.append(self)

    def is_leaf(self):
        return not bool(self.children)


def nop(*_):
    pass


def phylo2tn(phylo_tree):
    phylo_root = phylo_tree.root
    root = TreeNode(phylo_root.name)
    to_process = [(root, phylo_root)]
    while to_process:
        n_to_process = []
        for tn, pn in to_process:
            for clade in pn.clades:
                cn = TreeNode(clade.name, tn)
                n_to_process.append((cn, clade))
        to_process = n_to_process
    return root


def draw_node(node):
    print node.node, ":", node.in_edge,
    if not node.is_leaf():
        print "(",
        for i, child in enumerate(node.children):
            draw_node(child)
            if i != len(node.children) - 1:
                print ",",
        print ")",


def construct_dict(species):
    n = len(species)
    k = random.randint(n, 4*n)
    return {s: random.randint(n, n*n) for i, s in enumerate(species)}


def visited_dict(tree):
    visited = {}
    goto = [tree]
    while goto:
        n_goto = []
        for node in goto:
            visited[node] = False
            for child in node.children:
                n_goto.append(child)
        goto = n_goto
    return visited


def root_tree(tree, specie):
    def find_specie(node, visited, specie):
        visited[node] = True
        if node.is_leaf() and node.node == specie:
            return node
        for child in node.children:
            if not visited[child]:
                node = find_specie(child, visited, specie)
                if node:
                    return node
        return None
    
    def root_tree_node(node, old_node, visited):
        visited[old_node] = True
        for child in old_node.children:
            if not visited[child]:
                child_node = TreeNode(child.node, node)
                root_tree_node(child_node, child, visited)
        if old_node.parent and not visited[old_node.parent]:
            child_node = TreeNode(old_node.parent.node, node)
            root_tree_node(child_node, old_node.parent, visited)

    visited = visited_dict(tree)
    s_node = find_specie(tree, visited, specie)
    if not s_node:
        return None
    visited = {v: False for v in visited}
    root_node = TreeNode(s_node.node)
    root_tree_node(root_node, s_node, visited)
    return root_node


def dfs(node, fun_pre=nop, fun_post=nop):
    def internal_dfs(node, visited, fun_pre, fun_post):
        visited[node] = True
        fun_pre(node)
        for child in node.children:
            if not visited[child]:
                internal_dfs(child, visited, fun_pre, fun_post)
        fun_post(node)

    internal_dfs(node, visited_dict(node), fun_pre, fun_post)


def label_edges(tree, d):
    result = []

    def label_leaf(node):
        if node.is_leaf():
            node.in_edge = d[node.node]

    def label_internal(node):
        if node.is_leaf():
            return
        xor_list = []
        for child in node.children:
            if child.in_edge is None:
                break
            xor_list.append(child.in_edge)
        else:
            node.in_edge = reduce(lambda x, y: x ^ y, xor_list)

    def append_to_result(node):
        if not node.is_leaf() and node.parent != tree and node != tree:
            result.append(node.in_edge)

    dfs(tree, label_leaf)
    dfs(tree, fun_post=label_internal)
    dfs(tree, fun_post=append_to_result)
    return set(result)


def process(species_s, tree1_s, tree2_s):
    species = species_s.split()
    tree1 = root_tree(phylo2tn(Phylo.read(StringIO(tree1_s), "newick")), species[0])
    tree2 = root_tree(phylo2tn(Phylo.read(StringIO(tree2_s), "newick")), species[0])

    # draw_node(tree1)
    # print ""
    # draw_node(tree2)
    # print ""

    d = construct_dict(species)
    set1 = label_edges(tree1, d)
    set2 = label_edges(tree2, d)

    # draw_node(tree1)
    # print ""
    # draw_node(tree2)
    # print ""

    # print set1
    # print set2
    print 2 * (len(species) - 3) - 2 * len(set1 & set2)


def main():
    s = raw_input()
    if s == '1':
        fd = open(sys.argv[1], "r")
        lines = fd.readlines()
        fd.close()
        process(lines[0], lines[1], lines[2])
    else:
        process("dog rat elephant mouse cat rabbit",
                "(rat,(dog,cat),(rabbit,(elephant,mouse)));",
                "(rat,(cat,dog),(elephant,(mouse,rabbit)));")


if __name__ == "__main__":
    main()