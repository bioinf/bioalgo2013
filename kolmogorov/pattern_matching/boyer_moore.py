def bad_char_tbl(string):
	table = {}
	prev = {}
	str_len = len(string)
	for i, c in enumerate(string):
		if not c in table:
			table[c] = [0] * str_len
		if not c in prev:
			prev[c] = -1
			table[c][0 : i + 1] = [0] * (i + 1)
		else:
			table[c][prev[c] + 1 : i + 1] = [prev[c]] * (i - prev[c])
		prev[c] = i

	for c in table:
		table[c][prev[c] + 1 : str_len] = [prev[c]] * (str_len - prev[c] - 1)

	return (lambda c, pos : table[c][pos] if c in table else 0)

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

def good_suffix_main(string):
	res = [-1] * len(string)
	str_len = len(string)
	z = z_function(string[::-1])[::-1]
	for i in xrange(str_len - 1):
		if z[i] != 0:
			res[str_len - z[i]] = i
	return res

def good_suffix_fail(string):
	res = [0] * len(string)
	str_len = len(string)
	zr = z_function(string)[::-1]
	largest = 0
	for i, z in enumerate(zr):
		if z - i == 1:
			largest = max(z, largest)
		res[-i - 1] = largest
	return res


def boyer_moore(text, pattern):
	bad_char = bad_char_tbl(pattern)
	suff_main = good_suffix_main(pattern)
	suff_fail = good_suffix_fail(pattern)
	matches = []

	k = len(pattern) - 1
	prev_k = -1
	while k < len(text):
		i = len(pattern) - 1
		h = k
		while i >= 0 and text[h] == pattern[i]:
			i -= 1
			h -= 1
		if i == -1: 	#match
			matches.append(k - len(pattern) + 1)
			k += len(pattern) - suff_fail[1] if len(pattern) > 1 else 1
		else: 						#missmatch
			#good suffix
			if i == len(pattern) - 1:
				suff_shift = 1
			elif suff_main[i + 1] != -1:
				suff_shift = len(pattern) - 1 - suff_main[i + 1]
			else:
				suff_shift = len(pattern) - 1 - suff_fail[i + 1]
			#bad character
			char_shift = i - bad_char(text[h], i)
			shift = max(char_shift, suff_shift)
			if shift >= i + 1:
				prev_k = k
			k += shift
	return matches
