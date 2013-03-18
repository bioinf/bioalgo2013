# -*- coding: utf-8 -*-

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

def kmp_z( text, pattern ):
	result = []
	z = z_func(pattern + "$" + text)

	pat_len = len(pattern)
	z_len   = len(z)

	for i in xrange(pat_len,z_len):
		if z[i] == pat_len:
			result.append(i-pat_len-1)
	return result

def main():
	text    = raw_input()
	pattern = raw_input()
	
	print kmp_z(text, pattern)

if __name__ == "__main__":
	main()