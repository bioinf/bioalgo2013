from Bio.SubsMat import MatrixInfo
import sys

def getScore( s1, s2, matrix, gap ):
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

    return score[M][N]

def readFASTA( fileName ):
    fastaDict = {}

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

            fasta_name = line[1:].strip()
            fasta_seq = ""
        else:
            fasta_seq += line.strip()

    if fasta_name != "":
        for rep in replaceList:
            fasta_seq = fasta_seq.replace(rep, "")
        fastaDict[fasta_name] = fasta_seq

    fd.close()

    return fastaDict

def main():
    matrix = MatrixInfo.blosum62
    gap = -5

    fd = readFASTA(sys.argv[1])
    l = fd.values()

    print getScore(l[0], l[1], matrix, gap)

if __name__ == "__main__":
    main()

