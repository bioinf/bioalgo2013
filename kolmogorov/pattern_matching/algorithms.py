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
	#counter = 0
	while i + j < len(string):
		#counter += 1
		#print j
		if string[i + j] == pattern[j]:
			if j == len(pattern) - 1:
				#print j 
				found.append(i)
				i = i + j - pfun[j - 1]
				j = pfun[j - 1]
			else:
				j += 1
		else:
			if j == 0:
				i += 1
			else:
				i = i + j - pfun[j - 1]
				j = pfun[j - 1]

	#print counter
	return found

################

def hash_str(string, p, mod = 1000001):
	pp = 1
	h = 0
	for i in xrange(len(string) - 1, -1, -1):
		h = (h + ord(string[i]) * pp) % mod
		pp *= p
	return h

def karp(string, pattern):
	P = 31
	mod = 1000001
	p_len = len(pattern)
	h = hash_str(string[0 : p_len], P)
	pat_h = hash_str(pattern, P)
	found = [0] if h == pat_h and pattern == string[0 : p_len] else []
	for i in xrange(p_len, len(string)):
		pp = pow(P, p_len, mod)
		h = h * P - ord(string[i - p_len]) * pp  + ord(string[i])
		h %= mod 
		#print h
		if h == pat_h and string[i - p_len + 1 : i + 1] == pattern:
			found.append(i - p_len + 1)
	return found

################

def naive(string, pattern):
	res = []
	#counter = 0
	for i in xrange(0, len(string) - len(pattern) + 1):
		fail = False
		for k in xrange(i, i + len(pattern)):
			#counter += 1
			if (string[k] != pattern[k - i]):
				fail = True
				break
		if not fail:
			res.append(i)
	#print counter
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

