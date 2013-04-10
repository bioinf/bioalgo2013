# -*- coding: utf-8 -*-

def prefix (string):
	result = [0]
	n = len(string)

	for i in xrange(1, n):
		j = result[i-1]
		while j > 0 and string[i] != string[j]:
			j = result[j-1]

		result.append(j + (string[i] == string[j]))

	return result

def kmp_prefix (string, sub):
	n, m = len(string), len(sub)
	result = []
	final = sub + '$' + string
	pref = prefix(final)
	print pref

	for i in xrange(m+1, m+n+1):
		if pref[i] == m:
			result.append(i-m)

	return result

	

def z_function (string):
	n = len(string)
	result = [n]
	L = 0
	R = 0

	for i in xrange(1, n):
		if i >= R:
			c = i
			while c != n and string[c] == string[c-i]:
				c += 1
			result.append(c-i)
			L = i
			R = c
		else:
			j = result[i-L]
			if i + j < R:
				result.append(j)
			else:
				c = R
				while c != n and string[c] == string[c-i]:
					c += 1
				result.append(c-i)
				L = i
				R = c

	return result

def kmp_z (string, sub):
	n, m = len(string), len(sub)
	final = sub + '$' + string
	Z = z_function(final)
	print final
	print Z
	result = []
	for i in xrange(m, n+m):
		if Z[i] == m:
			result.append(i-m-1)
	return result