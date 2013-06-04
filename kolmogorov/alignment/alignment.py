#!/usr/bin/env python

import Bio.SubsMat.MatrixInfo as sbsmat
from Bio import SeqIO
import sys

def readFASTA(filename):
    fastaList = []
    fd = open(filename, "r")
    seqs = SeqIO.parse(fd, "fasta")
    for seq in seqs:
        fastaList.append(seq.seq)
    fd.close()
    return fastaList

def global_score(seq1, seq2, gap, subs_matrix):
	len1 = len(seq1)
	len2 = len(seq2)

	mat = [[0 for x in xrange(len2 + 1)] for x in xrange(len1 + 1)]
	for i in xrange(len1 + 1):
		mat[i][0] = i * gap
	
	for i in xrange(1, len1 + 1):
		for j in xrange(1, len2 + 1):
			mat[0][j] = j * gap
			try:
				delta = subs_matrix[(seq1[i - 1], seq2[j - 1])]
			except:
				delta = subs_matrix[(seq2[j - 1], seq1[i - 1])]
			mat[i][j] = max(mat[i][j - 1] + gap, mat[i - 1][j] + gap, mat[i - 1][j - 1] + delta)
	
	return mat[len1][len2]


def local_align(seq1, seq2, gap, subs_matrix):
	len1 = len(seq1)
	len2 = len(seq2)

	mat = [[0 for x in xrange(len2 + 1)] for x in xrange(len1 + 1)]
	back = [[0 for x in xrange(len2 + 1)] for x in xrange(len1 + 1)]
	
	max_score = 0
	max_pos = 0, 0
	for i in xrange(1, len1 + 1):
		for j in xrange(1, len2 + 1):
			try:
				delta = subs_matrix[(seq1[i - 1], seq2[j - 1])]
			except:
				delta = subs_matrix[(seq2[j - 1], seq1[i - 1])]
			lst = [	0, 
					mat[i][j - 1] + gap, 
					mat[i - 1][j] + gap, 
					mat[i - 1][j - 1] + delta]
			m = max([ (lst[x], x) for x in xrange(len(lst)) ])

			mat[i][j] = m[0]
			if max_score < m[0]:
				max_score = m[0]
				max_pos = i, j

			back[i][j] = m[1]
	start, end = backtrack(mat, back, max_pos)
	return max_score, seq1[start[0] : end[0]], seq2[start[1] : end[1]]


def backtrack(score, matrix, pos):
	end = pos
	start = pos
	val = matrix[pos[0]][pos[1]]
	while val != 0:
		val = matrix[pos[0]][pos[1]]
		start = pos
		if val == 1:
			pos = pos[0], pos[1] - 1
		elif val == 2:
			pos = pos[0] - 1, pos[1]
		else:
			pos = pos[0] - 1, pos[1] - 1
	return start, end


def glob_affine_gap(seq1, seq2, subs_matrix, gap_open, gap_ext):
	len1 = len(seq1)
	len2 = len(seq2)

	s_m = [[float("-inf") for x in xrange(len2 + 1)] for x in xrange(len1 + 1)]
	s_x = [[float("-inf") for x in xrange(len2 + 1)] for x in xrange(len1 + 1)]
	s_y = [[float("-inf") for x in xrange(len2 + 1)] for x in xrange(len1 + 1)]
	b_m = [[0 for x in xrange(len2 + 1)] for x in xrange(len1 + 1)]
	b_x = [[0 for x in xrange(len2 + 1)] for x in xrange(len1 + 1)]
	b_y = [[0 for x in xrange(len2 + 1)] for x in xrange(len1 + 1)]
	s_m[0][0] = 0

	for i in xrange(len1 + 1):
		s_x[i][0] = gap_open + (i - 1) * gap_ext
	for i in xrange(len2 + 1):
		s_y[0][i] = gap_open + (i - 1) * gap_ext
	
	for i in xrange(1, len1 + 1):
		for j in xrange(1, len2 + 1):
			try:
				delta = subs_matrix[(seq1[i - 1], seq2[j - 1])]
			except:
				delta = subs_matrix[(seq2[j - 1], seq1[i - 1])]
			lst_m = [s_m[i - 1][j - 1] + delta, s_x[i - 1][j - 1] + delta, s_y[i - 1][j - 1] + delta]
			lst_x = [s_m[i - 1][j] + gap_open, s_x[i - 1][j] + gap_ext, s_y[i - 1][j] + gap_open]
			lst_y = [s_m[i][j - 1] + gap_open, s_x[i][j - 1] + gap_open, s_y[i][j - 1] + gap_ext]

			s_m[i][j] = max(lst_m)
			s_x[i][j] = max(lst_x)
			s_y[i][j] = max(lst_y)

			b_m[i][j] = lst_m.index(s_m[i][j])
			b_x[i][j] = lst_x.index(s_x[i][j])
			b_y[i][j] = lst_y.index(s_y[i][j])

	#backtracking
	all_mat = [s_m, s_x, s_y]
	i, j = len1, len2
	matrix = max(s_m, s_x, s_y, key = lambda x : x[i][j])
	score = matrix[-1][-1]
	res1, res2 = "", ""
	while i != 0 and j != 0:
		if matrix == s_m:
			res1 += seq1[i - 1]
			res2 += seq2[j - 1]
			matrix = all_mat[b_m[i][j]]
			i -= 1
			j -= 1
		elif matrix == s_x:
			res1 += seq1[i - 1]
			res2 += "-"
			matrix = all_mat[b_x[i][j]]
			i -= 1
		elif matrix == s_y:
			res1 += "-"
			res2 += seq2[j - 1]
			matrix = all_mat[b_y[i][j]]
			j -= 1
	return score, res1[::-1], res2[::-1]


def main():
	seqs = readFASTA(sys.argv[1])
	#print global_score(str(seqs[0]), str(seqs[1]), -5, sbsmat.blosum62)
	#print local_align(str(seqs[0]), str(seqs[1]), -5, sbsmat.pam250)
	aln = glob_affine_gap(str(seqs[0]), str(seqs[1]), sbsmat.blosum62, -11, -1)
	print "{0}\n{1}\n{2}".format(*aln)


if __name__ == "__main__":
	main()
