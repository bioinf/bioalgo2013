from Bio.SubsMat import MatrixInfo
import sys

def getGlobalScore( s1, s2, matrix, gap ):
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
            try:
                m = matrix[(s1[i-1], s2[j-1])]
            except:
                m = matrix[(s2[j-1], s1[i-1])] 

            score[i][j] = max(score[i-1][j] + gap,
                              score[i][j-1] + gap,
                              score[i-1][j-1] + m)

    return score

def getLocalScore( s1, s2, matrix, gap ):
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
            try:
                m = matrix[(s1[i-1], s2[j-1])]
            except:
                m = matrix[(s2[j-1], s1[i-1])] 

            l = [0, score[i-1][j] + gap, score[i][j-1] + gap, score[i-1][j-1] + m]
            score[i][j] = max(l)
            if l.index(score[i][j]) == 1:
                from_s[i][j] = [i-1, j]
            elif l.index(score[i][j]) == 2:
                from_s[i][j] = [i, j-1]
            elif l.index(score[i][j]) == 3:
                from_s[i][j] = [i-1, j-1]

    return score, from_s

def getLocalMax( score ):
    r = float("-inf")
    k,l = 0,0
    for i in xrange(len(score)):
        r_ = max(score[i])
        if r_ > r:
            r = r_
            k = i
            l = score[i].index(r_)

    return r, (k,l)

def getLocalCoords( from_s, (k, l) ):
    i,j = k,l
    while from_s[i][j] != []:
        i,j = from_s[i][j][0],from_s[i][j][1]
    return (i,j),(k,l)

def readFASTA( fileName ):
    fastaDict = {}
    fastaList = []

    replaceList = [" ", "\r", "\n"]
    stripList = [" ", "-", "_", "[", "<", "("]

    fd = open(fileName, "r")

    fasta_name = ""
    fasta_seq = ""
    for line in fd:
        if line.startswith(">"):
            if fasta_name != "":
                for rep in replaceList:
                    fasta_seq = fasta_seq.replace(rep, "")
                fastaDict[fasta_name] = fasta_seq
                fastaList.append(fasta_seq)

            fasta_name = line[1:].strip()
            fasta_seq = ""
        else:
            fasta_seq += line.strip()

    if fasta_name != "":
        for rep in replaceList:
            fasta_seq = fasta_seq.replace(rep, "")
        fastaDict[fasta_name] = fasta_seq
        fastaList.append(fasta_seq)

    fd.close()

    return fastaDict,fastaList

def main():
    matrix_blo = MatrixInfo.blosum62
    matrix_pam = MatrixInfo.pam250
    gap = -5

    l = readFASTA(sys.argv[1])[1]

    print "GLOBAL ALIGNMENT"
    score = getGlobalScore(l[0], l[1], matrix_blo, gap)
    print score[len(l[0])][len(l[1])]

    print "LOCAL ALIGNMENT"
    score,from_s = getLocalScore(l[0], l[1], matrix_pam, gap)

    # print "      0",
    # for i in xrange(len(l[1])):
    #     print "{0:2d}".format(i + 1),
    # print ""
    # print "       ",
    # for i in l[1]:
    #     print " {0}".format(i),
    # print ""
    # for i in xrange(len(score)):
    #     if i != 0:
    #         print "{0:2d} {1}".format(i, l[0][i-1]),
    #     else:
    #         print " 0  ",
    #     for j in score[i]:
    #         print "{0:2d}".format(j),
    #     print ""

    m =  getLocalMax(score)
    print m[0]
    coords = getLocalCoords(from_s, m[1])
    print l[0][coords[0][0]:coords[1][0]]
    print l[1][coords[0][1]:coords[1][1]]

if __name__ == "__main__":
    main()

