# -*- coding: utf-8 -*-

import operator
import sys

import numpy as np
from Bio import SeqIO
from Bio.SubsMat.MatrixInfo import blosum62


for x, y in blosum62.keys():
    blosum62[y, x] = blosum62[x, y]


def needleman_wunsch(seq1, seq2, gap_penalty=-5):
    m, n = len(seq1), len(seq2)
    d = np.zeros((m + 1, n + 1))
    d[:, 0] = np.arange(m + 1) * gap_penalty
    d[0, :] = np.arange(n + 1) * gap_penalty

    for i in xrange(1, m + 1):
        for j in xrange(1, n + 1):
            ch1, ch2 = seq1[i - 1], seq2[j - 1]
            d[i, j] = max(d[i - 1, j] + gap_penalty,  # del
                          d[i, j - 1] + gap_penalty,  # ins
                          d[i - 1, j - 1] + blosum62[ch1, ch2])

    return int(d[m, n])


def main():
    seq1, seq2 = SeqIO.parse(sys.stdin, "fasta")
    print(needleman_wunsch(seq1, seq2))


if __name__ == "__main__":
    main()
