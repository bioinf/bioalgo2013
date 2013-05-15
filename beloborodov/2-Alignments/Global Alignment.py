from Bio import SeqIO
from Bio.SubsMat.MatrixInfo import blosum62

seq1, seq2 = SeqIO.parse(open('GLOB_in'), "fasta")
m, n = len(seq1)+1, len(seq2)+1

a = list([0]*m for i in range(n))

gap_penalty = -5

for i in range(m):
    a[0][i] = i * gap_penalty
for i in range(n):
    a[i][0] = i * gap_penalty

for i in range(1, n):
    for j in range(1, m):
        ch1, ch2 = seq1[j - 1], seq2[i - 1]
        try:
            blosum = blosum62[ch1, ch2]
        except:
            blosum = blosum62[ch2, ch1]
        a[i][j] = max(a[i - 1][j - 1] + blosum,
                    a[i - 1][j] + gap_penalty,
                    a[i][j - 1] + gap_penalty)
print(a[n-1][m-1])
