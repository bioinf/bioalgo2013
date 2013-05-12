# -*- coding: utf-8 -*-

from __future__ import print_function

import sys

import numpy as np
from Bio import SeqIO
from Bio.SubsMat.MatrixInfo import blosum62


for x, y in blosum62.keys():
    blosum62[y, x] = blosum62[x, y]


def needleman_wunsch(seq1, seq2, gap_open, gap_extend=0):
    m, n = len(seq1), len(seq2)
    v = np.zeros((m + 1, n + 1))
    e = np.zeros((m + 1, n + 1))
    f = np.zeros((m + 1, n + 1))

    v[:, 0] = -gap_open - np.arange(0, m + 1) * gap_extend
    v[0, :] = -gap_open - np.arange(0, n + 1) * gap_extend
    v[0, 0] = 0

    e[:, 0] = -float("inf")
    f[0, :] = -float("inf")
    e[0, 0] = f[0, 0] = 0

    for i in xrange(1, m + 1):
        for j in xrange(1, n + 1):
            ch1, ch2 = seq1[i - 1], seq2[j - 1]
            e[i, j] = max(e[i, j - 1] - gap_extend, v[i, j - 1] - gap_open)
            f[i, j] = max(f[i - 1, j] - gap_extend, v[i - 1, j] - gap_open)
            v[i, j] = max(e[i, j], f[i, j],
                          v[i - 1, j - 1] + blosum62[ch1, ch2])

    return v, e, f


def trace(seq1, seq2, v, e, f, gap_open, gap_extend=0):
    tmp1, tmp2 = [], []
    i, j = len(seq1), len(seq2)

    while i or j:
        ch1, ch2 = seq1[i - 1], seq2[j - 1]
        if v[i, j] in [v[i, j - 1] - gap_open, e[i, j - 1] - gap_extend]:
            tmp1.append("-")
            tmp2.append(ch2)
            j -= 1
        elif v[i, j] in [v[i - 1, j] - gap_open, f[i - 1, j] - gap_extend]:
            tmp1.append(ch1)
            tmp2.append("-")
            i -= 1
        elif v[i, j] == v[i - 1, j - 1] + blosum62[ch1, ch2]:
            tmp1.append(ch1)
            tmp2.append(ch2)
            i -= 1
            j -= 1
        else:
            assert False  # Impossible.

    return "".join(reversed(tmp1)), "".join(reversed(tmp2))


def main():
    gap_open, gap_extend = 11, 1

    seq1, seq2 = SeqIO.parse(sys.stdin, "fasta")
    v, e, f = needleman_wunsch(seq1, seq2, gap_open, gap_extend)
    score = int(v[-1, -1])
    print(score)
    tr1, tr2 = trace(seq1, seq2, v, e, f, gap_open, gap_extend)
    print(tr1, tr2, sep="\n")



if __name__ == "__main__":
    main()
