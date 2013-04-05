def hash_t( text, length, coef = 17, module = 1000001 ):
	if len(text) < length:
		return None

	return sum(pow(coef, length-1-i, module)*ord(text[i]) for i in xrange(length)) % module

def hash_next( h, first, next, length, coef = 17, module = 1000001 ):
	hnew = h - pow(coef, length-1, module) * ord(first)
	hnew *= coef
	hnew += ord(next)
	hnew %= module

	return hnew

def rabin_karp( text, pattern ):
	result = []

	pat_len = len(pattern)
	txt_len = len(text)
	h       = hash_t(pattern, pat_len)
	hw      = hash_t(text, pat_len)

	if hw == None:
		return result

	for i in xrange(txt_len - pat_len):
		if h == hw:
			result.append(i)
		hw = hash_next(hw, text[i], text[i+pat_len],pat_len)
	return result

def main():
	text    = raw_input()
	pattern = raw_input()

	print rabin_karp(text, pattern)

if __name__ == "__main__":
	main()