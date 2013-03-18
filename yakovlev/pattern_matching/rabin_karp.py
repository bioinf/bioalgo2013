def hash( text, length, coef = 17, module = 1000001 ):
	result = []
	text_len = len(text)
	if text_len < length:
		return result

	result.append(sum([coef**(length-1-i)*ord(text[i]) for i in xrange(length)]) % module)
	for i in xrange(length, text_len):
		next = ( result[-1] - (coef**(length-1) * ord(text[i - length])) ) * coef
		next += ord(text[i])
		next %= module

		result.append(next)

	return result

def rabin_karp( text, pattern ):
	result = []

	pat_len = len(pattern)
	h       = hash(pattern, pat_len)[0]
	hashes  = hash(text, pat_len)
	h_len   = len(hashes)

	for i in xrange(h_len):
		if hashes[i] == h:
			result.append(i)
	return result 

def main():
	text    = raw_input()
	pattern = raw_input()

	print rabin_karp(text, pattern)

if __name__ == "__main__":
	main()