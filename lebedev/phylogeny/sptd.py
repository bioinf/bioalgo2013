# -*- coding: utf-8 -*-

import random
import sys

from dendropy import TreeList


def _hashtree(t, root_label, marks):
    def dfs(node):
        assert node is not None
        mark = marks[node.taxon.label] if node.is_leaf() else 0

        seen.add(node)
        for child in node.get_adjacent_nodes():
            if child in seen:
                continue

            mark ^= dfs(child)

        if node.is_internal() and node.parent_node is not None:
            splits.add(mark)

        return mark

    seen, splits = set(), set()
    dfs(t.find_node_with_taxon_label(root_label))
    return splits


def split_distance(t1, t2):
    taxon_labels = set(t1.taxon_set.labels()) | set(t2.taxon_set.labels())
    common_taxon_labels = set(t1.taxon_set.labels()) & \
                          set(t2.taxon_set.labels())
    n = len(taxon_labels)
    marks = {name: random.getrandbits(n)
             for idx, name in enumerate(taxon_labels)}

    root_label = random.choice(list(common_taxon_labels))
    splits1 = _hashtree(t1, root_label, marks)
    splits2 = _hashtree(t2, root_label, marks)
    return 2 * (n - 3) - 2 * len(splits1 & splits2)


if __name__ == "__main__":
    handle = sys.stdin
    _taxon_labels = next(handle)
    t1, t2 = TreeList.get_from_string("".join(handle), schema="newick")
    print(split_distance(t1, t2))
