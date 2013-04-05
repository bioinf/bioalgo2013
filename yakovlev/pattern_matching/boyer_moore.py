# -*- coding: utf-8 -*-

###############################

def next_char_pos( bcp, ch, pos ):
	if bcp is None or ch not in bcp:
		return -1
	for i in bcp[ch]:
		if i < pos:
			return i

def bad_char_preprocessing( pattern ):
	if len(pattern) == 0:
		return
	res = {a : [-1] for a in pattern}
	for i,c in enumerate(pattern):
		res[c].append(i)
	res = {a : res[a][::-1] for a in res}
	return (lambda ch, pos : next_char_pos(res, ch, pos))

###############################

def z_func( text ):
	text_len = len(text)
	
	z = [0 for i in xrange(text_len)]
	z[0] = text_len
	
	left,right = 0,0
	for i in xrange(1,text_len):
		if i > right:
			j = 0
			while (i + j) < text_len and text[i + j] == text[j]:
				j += 1
			z[i] = j
			left = i
			right = i + j - 1
		else:
			if z[i - left] < right - i + 1:
				z[i] = z[i - left]
			else:
				j = 1
				while (j + right) < text_len and text[right + j] == text[right - i + j]:
					j += 1
				z[i] = right - i + j
				left = i
				right += j - 1
	return z

def good_suffix_preprocessing( pattern ):
	res = [-1 for c in pattern]

	patt_len = len(pattern)
	z = z_func(pattern[::-1])[::-1]

	for i in xrange(patt_len - 1):
		if z[i] != 0:
			res[patt_len - z[i]] = i
	return res

def full_shift( pattern ):
	res = [0 for c in pattern]

	patt_len = len(pattern)
	zr = z_func(pattern)[::-1]
	l = 0

	for i,z in enumerate(zr):
		if z - i == 1:
			l = max(z, l)
		res[-(i+1)] = l
	return res

###############################

def boyer_moore( text, pattern ):
	result = []

	patt_len = len(pattern)
	text_len = len(text)

	if text_len == 0 or patt_len == 0 or patt_len > text_len:
		return result

	bcr = bad_char_preprocessing(pattern)
	gsp = good_suffix_preprocessing(pattern)
	fs = full_shift(pattern)

	rpos = len(pattern) - 1
	while rpos < text_len:
		for k in xrange(len(pattern)):
			pos = patt_len - k - 1
			bc_shift = 0
			gs_shift = 0
			
			if text[rpos - k] != pattern[pos]:
				# Bad character rule
				bc_shift = pos - bcr(text[rpos - k], pos)
			
				nk = patt_len - 1 - k
				# Good suffix rule
				if nk == patt_len - 1:
					gs_shift = 1
				elif gsp[nk+1] == -1:
					gs_shift = patt_len - fs[nk+1]
				else:
					gs_shift = patt_len - gsp[nk+1]

				shift = max(bc_shift, gs_shift)
				if shift:
					rpos += shift
					break
		else:
			result.append(rpos - patt_len + 1)
			rpos += 1

	return result


def main():
	text    = raw_input()
	pattern = raw_input()

	print boyer_moore(text, pattern)

if __name__ == "__main__":
	main()