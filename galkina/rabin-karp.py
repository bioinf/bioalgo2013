# -*- coding: utf-8 -*-

def hash (string, m):
	n = len(string)
	s = [ord(i) for i in string]
	result = []

	for k in xrange(n-m+1):
		if k == 0:
			result.append(sum(s[:m]))
		else:
			result.append(result[-1] + s[k+m-1] - s[k-1])
	return result

def rabin_karp (string, sub):
	result = []

	n, m = len(string), len(sub)
	H = sum(ord(i) for i in sub)
	h = hash(string, m)

	for k in xrange(n-m+1):
		if h[k] == H:
			for i in xrange(m):
				if string[k+i] != sub[i]:
					break
				elif i == m-1:
					result.append(k)
	return result