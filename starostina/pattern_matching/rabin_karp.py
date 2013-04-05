B = 37

def rolling_hash(pattern):
	hs = 0
	for c in pattern:
		hs = hs * B + ord(c)
	return hs

def next_hash(text, ind, pattern_len, prev, bn):
	return (prev - text[ind - 1]*bn) * B + ord(text[ind + pattern_len])

def rabin_karp(text, pattern):
	found_pos = []
	text_len = len(text)
	pattern_len = len(pattern)
	pattern_hash = rolling_hash(pattern)
	frame_hash = rolling_hash(text[:pattern_len])
	bn = B ** (pattern_len - 1)
	for i in xrange(text_len - pattern_len + 1):
		if (frame_hash == pattern_hash):
			found_pos.append(i)
		if (i < text_len - pattern_len):
			frame_hash = (frame_hash - ord(text[i]) * bn) * B + ord(text[i + pattern_len])
	return found_pos

if (__name__ == "__main__"):
	text = raw_input()
	pattern = raw_input()
	print rabin_karp(text, pattern)
