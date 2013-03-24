# -*- coding: utf-8 -*-

def prefix_function( text ):
	text_len = len(text)
	prefix   = [0 for i in xrange(text_len)]

	for i in xrange(1,text_len):
		c  = prefix[i - 1]
		while c != 0 and text[i] != text[c]:
			c  = prefix[c-1]

		prefix[i] = c + int(text[i] == text[c])

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