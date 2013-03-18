# -*- coding: utf-8 -*-

def prefix_function( text ):
	text_len = len(text)
	prefix   = [0 for i in xrange(text_len)]

	for i in xrange(1,text_len):
		mp = i - 1
		c  = prefix[mp]
		while c != 0 and text[i] != text[c]:
			mp = prefix[mp] - 1
			c  = prefix[mp]
		if c == 0:
			prefix[i] = int(text[c] == text[0])
		else:
			prefix[i] = c + 1

	return prefix


def kmp_prefix( text, pattern ):
	result = []
	prefix = prefix_function(pattern + "$" + text)

	pat_len = len(pattern)
	pre_len   = len(prefix)

	for i in xrange(2*pat_len,pre_len):
		if prefix[i] == pat_len:
			result.append(i-2*pat_len)
	return result

def main():
	text    = raw_input()
	pattern = raw_input()

	print kmp_prefix(text, pattern)

if __name__ == "__main__":
	main()