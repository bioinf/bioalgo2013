from sys import argv
import random
import time

def naive(s, t):
	match = []
	for i in range(len(s) - len(t) + 1):
		if s[i:i + len(t)] == t:
			match.append(i)
	return match
	
def prefix_function(s):
	p = [0] * len(s)
	for i in range(1, len(s)):
		p[i] = p[i - 1]
		while p[i] > 0 and s[i] != s[p[i]]:
			p[i] = p[p[i] - 1]
		if s[i] == s[p[i]]:
			p[i] += 1
	return p
	
def z_function(s):
	z = [0] * len(s)
	left, right = 0, 0
	for i in range(len(s)):
		if (i > right):
			j = 0
			while i + j < len(s) and s[j] == s[i + j]:
				j += 1
			z[i] = j
			left, right = i, i + j - 1
		elif z[i - left] < right - i + 1:
			z[i] = z[i - left]
		else:
			j = 1
			while j + right < len(s) and s[j + right - i] == s[right + j]:
				j += 1
			z[i] = right + j - i
			left, right = i, right + j - 1
	return z

def kmp(f, s, t):
	a = f (t + '#' + s)
	match = []
	for i in range(len(t) + 1, len(a)):
		if (a[i] == len(t)):
			if (f == z_function):
				match.append(i - len(t) - 1)
			else:
				match.append(i - 2 * len(t))
	return match

class hash:
	def __init__(self, hash_p, hash_m, s):
		self.power = [1]
		self.hash_m = hash_m
		n = len(s)
		while len(self.power) <= n:
			self.power.append(self.power[-1] * hash_p % hash_m)
		self.hashes = [0] * (n + 1)
		h = 0
		for i in range(n):
			h = ((h * hash_p) + ord(s[i])) % hash_m
			self.hashes[i + 1] = h
		
	def get_hash(self, left, right):
		return (self.hashes[right] - self.hashes[left] * self.power[right - left]) % self.hash_m

def rabin_karp(s, t):
	hash_p = 257
	hash_m = 10 ** 9 + 7
	slen = len(s)
	tlen = len(t)
	pattern_hash = hash(hash_p, hash_m, t).get_hash(0, tlen)
	text_hash = hash(hash_p, hash_m, s)
	match = []
	for i in range(slen - tlen + 1):
		if text_hash.get_hash(i, i + tlen) == pattern_hash:
			match.append(i)
		
	return match

def boyer_moore(s, t):
	tlen = len(t)
	slen = len(s)
	shift_one = {'A' : -1, 'C' : -1, 'G' : -1, 'T' : -1}
	for i in range(tlen - 1):
		shift_one[t[i]] = i
	z = z_function(t[::-1])
	max_z = 0
	shift_many = [1]
	for i in range(tlen):
		if max_z < z[i]:
			for j in range(max_z, z[i]):
				shift_many.append(i)
				max_z = z[i]
	for i in range(len(shift_many), tlen + 1):
		shift_many.append(1)
	
	match = []
	i = tlen - 1
	while i < slen:
		j = tlen - 1
		if (s[i] != t[j]):
			i += 1 if shift_one[s[i]] < 0 else (tlen - shift_one[s[i]] - 1)
		else:
			k = i
			while j >= 0 and s[k] == t[j]:
				j -= 1
				k -= 1
			if j == -1:
				match.append(i - tlen + 1)
				i += 1
			else:
				i += shift_many[j]
			
	return match		
	

def get_string(n, alp):
	return "".join(random.choice(alp) for _ in range(n))

def correct_test(n, m):
	nucleotids = ['A', 'T', 'G', 'C']
	
	while True:
		text = get_string(n, nucleotids)
		pattern = get_string(m, nucleotids)
		print ('test', text, pattern)
		m1 = naive(text, pattern)
		m2 = kmp(prefix_function, text, pattern)
		m3 = kmp(z_function, text, pattern)
		m4 = rabin_karp(text, pattern)
		m5 = boyer_moore(text, pattern)
		
		if (m1 != m2 or m2 != m3 or m3 != m4 or m4 != m5):
			print('test')
			print(text, pattern)
			print(m1)
			print(m2)
			print(m3)
			print(m4)
			print(m5)
			break

def main():
    n, m = argv[1:]
    correct_test(int(n), int(m))

if __name__ == "__main__":
    main()
