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
    dim = m + 1, n + 1
    e, backe = np.zeros(dim), np.zeros(dim, dtype="S2")
    f, backf = np.zeros(dim), np.zeros(dim, dtype="S2")
    v, backv = np.zeros(dim), np.zeros(dim, dtype="S2")

    v[:, 0] = -gap_open - np.arange(0, m + 1) * gap_extend
    v[0, :] = -gap_open - np.arange(0, n + 1) * gap_extend
    v[0, 0] = 0

    e[:, 0] = -float("inf")
    f[0, :] = -float("inf")
    e[0, 0] = f[0, 0] = 0

    for i in xrange(1, m + 1):
        for j in xrange(1, n + 1):
            ch1, ch2 = seq1[i - 1], seq2[j - 1]
            e[i, j], backe[i, j] = max(
                (e[i, j - 1] - gap_extend, "d<"),
                (v[i, j - 1] - gap_open, "m<"))
            f[i, j], backf[i, j] = max(
                (f[i - 1, j] - gap_extend, "i^"),
                (v[i - 1, j] - gap_open, "m^"))
            v[i, j], backv[i, j] = max(
                (e[i, j], backe[i, j]),
                (f[i, j], backf[i, j]),
                (v[i - 1, j - 1] + blosum62[ch1, ch2], "m\\"))

    return int(v[-1, -1]), (backe, backf, backv)


def trace(seq1, seq2, (backe, backf, backv)):
    tmp1, tmp2 = [], []
    i, j = len(seq1), len(seq2)

    back = backv
    while i and j:
        ch1, ch2 = seq1[i - 1], seq2[j - 1]
        current = back[i, j]
        if "<" in current:
            tmp1.append("-")
            tmp2.append(ch2)
            j -= 1
        elif "^" in current:
            tmp1.append(ch1)
            tmp2.append("-")
            i -= 1
        elif "\\" in current:
            tmp1.append(ch1)
            tmp2.append(ch2)
            i -= 1
            j -= 1
        else:
            assert False

        if "m" in current:
            back = backv
        elif "i" in current:
            back = backf
        else:
            back = backe

    return "".join(reversed(tmp1)), "".join(reversed(tmp2))


def main():
    gap_open, gap_extend = 11, 1

    seq1, seq2 = SeqIO.parse(sys.stdin, "fasta")
    score, back = needleman_wunsch(seq1, seq2, gap_open, gap_extend)
    print(score)
    tr1, tr2 = trace(seq1, seq2, back)
    print(tr1)
    print(tr2)



if __name__ == "__main__":
    main()
