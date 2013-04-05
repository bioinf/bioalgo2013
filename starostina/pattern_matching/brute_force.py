def brute_force(text, pattern):
	res = []
	text_len = len(text)
	pattern_len = len(pattern)

	for i in xrange(text_len - pattern_len + 1):
		if (all(text[i + j] == pattern[j] for j in xrange(pattern_len))):
			res.append(i)
	return res

if (__name__ == "__main__"):
	text = raw_input()
	pattern = raw_input()
	print brute_force(text, pattern)
