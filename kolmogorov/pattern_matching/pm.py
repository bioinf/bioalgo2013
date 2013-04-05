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
	while i + j < len(string):
		if string[i + j] == pattern[j]:
			if j == len(pattern) - 1:
				found.append(i)
				i = i + j - pfun[j]
				j = pfun[j]
			else:
				j += 1
		else:
			if j == 0:
				i += 1
			else:
				i = i + j - pfun[j - 1]
				j = pfun[j - 1]

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
	found = [0] if h == pat_h and pattern == string[0 : p_len] else []
	for i in xrange(p_len, len(string)):
		h = h * P - ord(string[i - p_len]) * (P ** p_len) + ord(string[i])
		if h == pat_h and string[i - p_len + 1 : i + 1] == pattern:
			found.append(i - p_len + 1)
	return found

def naive(string, pattern):
	res = []
	for i in xrange(len(string) - len(pattern) + 1):
		if string[i : i + len(pattern)] == pattern:
			res.append(i)
	return res

def z_function(string):
	z = [0] * len(string)
	z[0] = len(string)
	l, r = 0, 0
	for i in xrange(1, len(string)):
		if i <= r:
			z[i] = min(z[i - l], r - i + 1)
		while i + z[i] < len(string) and string[z[i]] == string[i + z[i]]:
			z[i] += 1
		if i + z[i] - 1 > r:
			l = i
			r = i + z[i] - 1
	return z

def z_find(string, pattern):
	found = []
	z_f = z_function(pattern + "$" + string)
	for i in xrange(len(pattern) + 1, len(z_f)):
		if z_f[i] == len(pattern):
			found.append(i - len(pattern) - 1)
	return found
	#for i in xrange(len(

print kmp   ("abraabcabcababcaba", "abcaba")
print karp  ("abraabcabcababcaba", "abcaba")
print naive ("abraabcabcababcaba", "abcaba")
print z_find("abraabcabcababcaba", "abcaba")
#print z_function("ababcaba")
#print prefixFunc("abcaba")
