import sys
from kmp import z_function

def bad_char_preproc(pattern):
	res = {}
	for i, c in enumerate(pattern):
		if c in res.keys():
			res[c].append(i)
		else:
			res[c] = [i]
	return res

def get_bad_char_shift(bc_dict, pattern, pos, ch):
	if ch in bc_dict.keys():
		for ind in bc_dict[ch][::-1]:
			if (ind < pos):
				return (pos - ind)
	return pos + 1

def good_suffix_preproc(pattern):
	pattern_len = len(pattern)
	z_f = z_function(pattern[::-1])
	res = [1] * pattern_len
	for i, z in enumerate(z_f):
		if not i or not z:
			continue
#		res[pattern_len - z] = pattern_len - i - z
		res[pattern_len - z] = max([i, res[pattern_len - z]])
	return res

def boyer_moore(text, pattern):
	pattern_len = len(pattern)
	text_len = len(text)
	bc_dict = bad_char_preproc(pattern)
	gs_arr = good_suffix_preproc(pattern)
	res = []
	i = 0
	while i <= text_len - pattern_len:
		match = True
		for j in xrange(pattern_len - 1, -1, -1):
			if (text[i + j] != pattern[j]):
				match = False
				bc_shift = get_bad_char_shift(bc_dict, pattern, j, text[i+j])
				gs_shift = gs_arr[j]
				i += max([gs_shift, bc_shift])
				break
		if match:
			res.append(i)
			i += 1
	return res

if __name__ == "__main__":
	text = raw_input()
	pattern = raw_input()
	print boyer_moore(text, pattern)
