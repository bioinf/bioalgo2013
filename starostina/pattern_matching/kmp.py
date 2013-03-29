def z_function(pattern):
	pattern_len = len(pattern)
	z = [0] * pattern_len
	z[0] = pattern_len
	l = 0
	r = 0
	for i in xrange(1, pattern_len):
		if (i > r):
			l = i
			r = i
			while (r < pattern_len and pattern[r] == pattern[r - i]):
				z[i] += 1
				r += 1
			r -= 1
		else:
			if (z[i - l] < r - i + 1):
				z[i] = z[i - l]
			else:
				l = i
				z[i] = r - i
				while (r < pattern_len and pattern[r] == pattern[r - i]): 
					r += 1
					z[i] += 1
				r -= 1
	return z

def prefix_function(pattern):
	pattern_len = len(pattern)
	prefix = [0] * pattern_len
	k = 0
	for i in xrange(1, pattern_len):
		while (k > 0 and pattern[k] != pattern[i]):
			k = prefix[k - 1]
		if (pattern[k] == pattern[i]):
			k += 1
		prefix[i] = k
	return prefix

def kmp_prefix(text, pattern):
	found_pos = []
	text_len = len(text)
	pattern_len = len(pattern)
	prefix = prefix_function(pattern + "$" + text)
	for i in xrange(2 * (pattern_len) - 1, pattern_len + text_len + 1):
		if (prefix[i] == pattern_len):
			found_pos.append(i - 2 * pattern_len)
	return found_pos

def kmp_z(text, pattern):
	found_pos = []
	text_len = len(text)
	pattern_len = len(pattern)
	z = z_function(pattern + "$" + text)
	for i in xrange(pattern_len + 1, text_len + 1):
		if (z[i] == pattern_len):
			found_pos.append(i - pattern_len - 1)
	return found_pos

if (__name__ == "__main__"):
	text = raw_input()
	pattern = raw_input()
	print kmp_prefix(text, pattern)
	print kmp_z(text, pattern)
