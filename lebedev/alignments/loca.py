# -*- coding: utf-8 -*-

from __future__ import print_function

import operator
import os
import sys

import numpy
from Bio import SeqIO
from Bio.SubsMat.MatrixInfo import pam250


for x, y in pam250.keys():
    pam250[y, x] = pam250[x, y]


SEQ_INS, SEQ_DEL, SEQ_MM = range(3)


def trace(d, (i, j), gap_penalty):
    path = []
    while d[i, j] and i and j:
        score = d[i, j]

        if score == d[i - 1, j] + gap_penalty:
            path.append((i, j, SEQ_INS))
            i -= 1
        elif score == d[i, j - 1] + gap_penalty:
            path.append((i, j, SEQ_DEL))
            j -= 1
        else:
            path.append((i, j, SEQ_MM))
            i -= 1
            j -= 1

    return path


def align(seq1, seq2, path):
    tmp1, tmp2 = [], []
    for i, j, direction in reversed(path):
        if direction == SEQ_DEL:
            tmp2.append(seq2[j - 1])
        elif direction == SEQ_INS:
            tmp1.append(seq1[i - 1])
        elif direction == SEQ_MM:
            tmp1.append(seq1[i - 1])
            tmp2.append(seq2[j - 1])

    return "".join(tmp1), "".join(tmp2)


def smith_waterman(seq1, seq2, gap_penalty=-5):
    m, n = len(seq1), len(seq2)
    d = numpy.zeros((m + 1, n + 1))

    best, pos = 0, (m, n)
    for i in xrange(1, m + 1):
        for j in xrange(1, n + 1):
            ch1, ch2 = seq1[i - 1], seq2[j - 1]
            d[i, j] = max(0,
                          d[i - 1, j] + gap_penalty,  # del
                          d[i, j - 1] + gap_penalty,  # ins
                          d[i - 1, j - 1] + pam250[ch1, ch2])

            if d[i, j] > best:
                best, pos = int(d[i, j]), (i, j)

    return best, trace(d, pos, gap_penalty)


def main():
    seq1, seq2 = SeqIO.parse(sys.stdin, "fasta")
    score, path = smith_waterman(seq1, seq2)
    print(score)
    print(*align(seq1, seq2, path), sep="\n")


if __name__ == "__main__":
    main()
