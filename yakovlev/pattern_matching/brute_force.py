# -*- coding: utf-8 -*-

def brute_force( text, pattern ):
	result = []

	text_len = len(text)
	patt_len = len(pattern)

	for i in xrange(text_len):
		k = i
		for j in xrange(patt_len):
			if k == text_len or pattern[j] != text[k]:
				break
			k += 1
		else:
			result.append(i)

	return result


def main():
	text    = raw_input()
	pattern = raw_input()

	print brute_force(text, pattern)

if __name__ == "__main__":
	main()