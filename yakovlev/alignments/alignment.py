import sys

from Bio.SubsMat import MatrixInfo
from Bio import SeqIO


def getScore(c1, c2, matrix):
    try:
        m = matrix[(c1, c2)]
    except:
        m = matrix[(c2, c1)]
    return m

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
    M = len(s1)
    N = len(s2)

    score_m = [[float("-inf") for j in xrange(N+1)] for i in xrange(M+1)]
    score_ix = [[float("-inf") for j in xrange(N+1)] for i in xrange(M+1)]
    score_iy = [[float("-inf") for j in xrange(N+1)] for i in xrange(M+1)]

    score_m[0][0] = 0
    score_ix[0][0] = gap_open
    score_iy[0] = [gap_open + i * gap_ext for i in xrange(N+1)]

    for i in xrange(1,M+1):
        score_ix[i][0] = score_ix[i-1][0] + gap_ext
        for j in xrange(1,N+1):
            m = getScore(s1[i-1], s2[j-1], matrix)
            score_m[i][j] = max(score_m[i-1][j-1],
                                score_ix[i-1][j-1],
                                score_iy[i-1][j-1]) + m
            score_ix[i][j] = max(score_m[i-1][j] + gap_open,
                                 score_ix[i-1][j] + gap_ext,
                                 score_iy[i-1][j] + gap_open)
            score_iy[i][j] = max(score_m[i][j-1] + gap_open,
                                 score_iy[i][j-1] + gap_ext,
                                 score_ix[i][j-1] + gap_open)

    return score_m, score_ix, score_iy

def makeGaps(s1, s2, score_m, score_ix, score_iy):
    l1 = list(s1)
    l2 = list(s2)

    i = len(s1)
    j = len(s2)
    
    while i != 0 or j != 0:
        l = [score_m[i][j], score_ix[i][j], score_iy[i][j]]
        p = l.index(max(l))
        if p == 0:
            i -= 1
            j -= 1
        elif p == 1:
            l2.insert(j, '-')
            i -= 1
        else:
            l1.insert(i, '-')
            j -= 1

    return "".join(l1), "".join(l2)

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

    l = readFASTA(sys.argv[1])
    M = len(l[0])
    N = len(l[1])

    print "GLOBAL ALIGNMENT"
    score = getGlobalScore(l[0], l[1], matrix_blo, gap)
    print score[M][N]
    # print ""

    print "LOCAL ALIGNMENT"
    score,from_s = getLocalScore(l[0], l[1], matrix_pam, gap)
    m = getLocalMax(score)
    print m[0]
    coords = getLocalCoords(from_s, m[1])
    print l[0][coords[0][0]:coords[1][0]]
    print l[1][coords[0][1]:coords[1][1]]
    print ""

    print "GLOBAL ALIGNMENT WITH AFFINE GAP PENALTY"
    score_m,score_ix,score_iy = getGlobalScoreAffine(l[0], l[1], matrix_blo, gap_open, gap_ext)

    print max(score_m[M][N], score_ix[M][N], score_iy[M][N])
    s1,s2 = makeGaps(l[0], l[1], score_m, score_ix, score_iy)
    print s1
    print s2


if __name__ == "__main__":
    main()
