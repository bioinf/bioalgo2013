import sys

import numpy as np

from Bio.SubsMat import MatrixInfo
from Bio import SeqIO


def getScore(c1, c2, matrix):
    try:
        m = matrix[(c1, c2)]
    except:
        m = matrix[(c2, c1)]
    return m

nucleomatrix = {(i, j): int(i == j) for i in "ACGT" for j in "ACGT"}

def getGlobalScore(s1, s2, matrix, gap):
    score = []

    M = len(s1)
    N = len(s2)

    for i in range(M+1):
        score.append([])
        for j in range(N+1):
            score[i].append(0)

    for j in range(1,N+1):
        score[0][j] = score[0][j-1] + gap

    for i in range(1,M+1):
        score[i][0] = score[i-1][0] + gap
        for j in range(1,N+1):
            m = getScore(s1[i-1], s2[j-1], matrix)
            score[i][j] = max(score[i-1][j] + gap,
                              score[i][j-1] + gap,
                              score[i-1][j-1] + m)

    return score


def getGlobalScoreAffine(s1, s2, matrix, gap_open, gap_ext):
    M, N = len(s1), len(s2)

    m = np.zeros((M + 1, N + 1))
    x = np.zeros((M + 1, N + 1))
    y = np.zeros((M + 1, N + 1))
    
    m[:, :] = float("-inf")
    x[:, :] = float("-inf")
    y[:, :] = float("-inf")
    m[0, 0] = 0

    fm = [[None for i in xrange(N + 1)] for j in xrange(M + 1)]
    fx = [[None for i in xrange(N + 1)] for j in xrange(M + 1)]
    fy = [[None for i in xrange(N + 1)] for j in xrange(M + 1)]

    x[:, 0] = gap_open + np.arange(0, M + 1) * gap_ext
    y[0, :] = gap_open + np.arange(0, N + 1) * gap_ext

    for i in xrange(1, M + 1):
        fx[i][0] = x
    for j in xrange(1, N + 1):
        fy[0][j] = y

    pos_value = [m, x, y]
    for i in xrange(1, M+1):
        for j in xrange(1, N+1):
            match = getScore(s1[i - 1], s2[j - 1], matrix)
            l_m = [m[i - 1, j - 1] + match, x[i - 1, j - 1] + match, y[i - 1, j - 1] + match]
            l_x = [m[i - 1, j] + gap_open, x[i - 1, j] + gap_ext, y[i - 1, j] + gap_open]
            l_y = [m[i, j - 1] + gap_open, x[i, j - 1] + gap_open, y[i, j - 1] + gap_ext]

            m[i, j] = max(l_m)
            x[i, j] = max(l_x)
            y[i, j] = max(l_y)

            fm[i][j] = pos_value[l_m.index(max(l_m))]
            fx[i][j] = pos_value[l_x.index(max(l_x))]
            fy[i][j] = pos_value[l_y.index(max(l_y))]

    # Traceback
    i, j = M, N
    res1, res2 = [], []
    l_max = [m[M, N], x[M, N], y[M, N]]
    current_matrix = pos_value[l_max.index(max(l_max))]
    while i != 0 and j != 0:
        if (current_matrix == m).all():
            res1.append(s1[i - 1])
            res2.append(s2[j - 1])
            current_matrix = fm[i][j]
            i -= 1
            j -= 1
        elif (current_matrix == x).all():
            res1.append(s1[i - 1])
            res2.append('-')
            current_matrix = fx[i][j]
            i -= 1
        elif (current_matrix == y).all():
            res1.append('-')
            res2.append(s2[j - 1])
            current_matrix = fy[i][j]
            j -= 1
        else:
            print "SH"
            exit()
    return "".join(res1[::-1]), "".join(res2[::-1]), int(max(l_max))


def getLocalScore(s1, s2, matrix, gap):
    score = []
    from_s = []

    M = len(s1)
    N = len(s2)

    for i in range(M+1):
        score.append([])
        from_s.append([])
        for j in range(N+1):
            score[i].append(0)
            from_s[i].append([])

    for i in range(1,M+1):
        for j in range(1,N+1):
            m = getScore(s1[i-1], s2[j-1], matrix)

            l = [0, score[i-1][j] + gap, score[i][j-1] + gap, score[i-1][j-1] + m]
            score[i][j] = max(l)
            if l.index(score[i][j]) == 1:
                from_s[i][j] = [i-1, j]
            elif l.index(score[i][j]) == 2:
                from_s[i][j] = [i, j-1]
            elif l.index(score[i][j]) == 3:
                from_s[i][j] = [i-1, j-1]

    return score, from_s


def getLocalMax(score):
    r = float("-inf")
    k,l = 0,0
    for i in xrange(len(score)):
        r_ = max(score[i])
        if r_ > r:
            r = r_
            k = i
            l = score[i].index(r_)

    return r, (k,l)


def getLocalCoords(from_s, (k, l)):
    i,j = k,l
    while from_s[i][j] != []:
        i,j = from_s[i][j][0],from_s[i][j][1]
    return (i,j),(k,l)


def readFASTA(fileName):
    fastaList = []
    fd = open(fileName, "r")
    seqs = SeqIO.parse(fd, "fasta")
    for seq in seqs:
        fastaList.append(seq.seq)
    fd.close()
    return fastaList

def checkScore( s1, s2, matrix, gap_open, gap_ext ):
    l = len(s1)
    score = 0

    for i in xrange(l):
        if s1[i] != '-' and s2[i] != '-':
            score += getScore(s1[i], s2[i], matrix)
        else:
            s = s1
            if s2[i] == '-':
                s = s2
            if s[i] == '-':
                if i == 0 or s[i-1] != '-':
                    score += gap_open
                else:
                    score += gap_ext
    return score

def main():
    matrix_blo = MatrixInfo.blosum62
    matrix_pam = MatrixInfo.pam250
    matrix_acgt = {('A', 'A') : 1, ('A', 'C') : 0, ('A', 'G') : 0, ('A', 'T') : 0,
                   ('C', 'C') : 1, ('C', 'G') : 0, ('C', 'T') : 0, 
                   ('G', 'G') : 1, ('G', 'T') : 0,
                   ('T', 'T') : 1}
    gap = -5
    gap_open = -11
    gap_ext = -1

    s1,s2 = readFASTA(sys.argv[1])

    print "GLOBAL ALIGNMENT"
    score = getGlobalScore(s1, s2, matrix_blo, gap)
    print score[-1][-1]
    print ""

    print "LOCAL ALIGNMENT"
    score,from_s = getLocalScore(s1, s2, matrix_pam, gap)
    loc_score, trace_matrix = getLocalMax(score)
    print loc_score
    coords = getLocalCoords(from_s, trace_matrix)
    print s1[coords[0][0]:coords[1][0]]
    print s2[coords[0][1]:coords[1][1]]
    print ""

    print "GLOBAL ALIGNMENT WITH AFFINE GAP PENALTY"
    r1,r2,score = getGlobalScoreAffine(s1, s2, matrix_blo, gap_open, gap_ext)
    print score
    print r1
    print r2
    # print checkScore(r1, r2, matrix_blo, gap_open, gap_ext)

if __name__ == "__main__":
    main()
