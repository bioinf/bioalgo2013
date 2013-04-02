#!/usr/bin/env python2

def prefixFunc(string):
	func = [0] * len(string)
	for i in xrange(1, len(string)):
		k = func[i - 1]
		while True:
			if string[i] == string[k]:
				func[i] = k + 1
				break
			if k == 0:
				func[i] = 0
				break
			k = func[k - 1]
	return func

def kmp(string, pattern):
	pfun = prefixFunc(pattern)
	i, j = 0, 0
	found = []
	while i + j < len(string) - 1:
		if string[i + j] == pattern[j]:
			if j == len(pattern) - 1:
				found.append(i)
				i = i + j - pfun[j]
				j = pfun[j]
				#break
			j += 1
		else:
			i = i + j - pfun[j]
			if j == 0:
				i += 1
			j = pfun[j]

	return found

def hash_str(string, p):
	pp = 1
	h = 0
	for i in xrange(len(string) - 1, -1, -1):
		h += ord(string[i]) * pp
		pp *= p
	return h


def karp(string, pattern):
	P = 31
	p_len = len(pattern)
	h = hash_str(string[0 : p_len], P)
	pat_h = hash_str(pattern, P)
	#print pat_h
	found = []
	for i in xrange(p_len, len(string)):
		hh = hash_str(string[i - p_len : i], P)
		#print h, hh
		if h == pat_h and string[i - p_len : i] == pattern:
			found.append(i - p_len)
		h = h * P - ord(string[i - p_len]) * (P ** p_len) + ord(string[i])
	return found

def naive(string, pattern):
	res = []
	for i in xrange(len(string) - len(pattern)):
		if string[i : i + len(pattern)] == pattern:
			res.append(i)
	return res

#print kmp("abracadabracada", "cad")
print kmp("abraabcabcabacada", "abc")
print karp("abraabcabcabacada", "abc")
print naive("abraabcabcabacada", "abc")
