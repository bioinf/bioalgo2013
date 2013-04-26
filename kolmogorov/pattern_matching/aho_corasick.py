#!/usr/bin/env python

class TrieNode:
	def __init__(self):
		self.links = {}
		self.fail = None
		self.pattern = None
		self.out = None
		
class Trie:
	def __init__(self):
		self.root = TrieNode()

	def add_pattern(self, pattern):
		node = self.root
		for sym in pattern:
			node = node.links.setdefault(sym, TrieNode())
		node.pattern = pattern

	def build_links(self):
		queue = []
		for node in self.root.links.values():
			node.fail = self.root
			queue.append(node)

		while len(queue) > 0:
			node = queue.pop(0)

			for sym, ch_node in node.links.iteritems():
				w = node.fail
				
				while (sym not in w.links) and w != None:
					assert w.fail != None
					w = w.fail

				ch_node.fail = w.links[sym] if w else self.root
				if ch_node.fail.pattern != None:
					ch_node.out = ch_node.fail
				elif ch_node.fail.out != None:
					ch_node.out = ch_node.fail.out

				queue.append(ch_node)

	def search_text(self, text):
		found = []
		node = self.root

		pos = 0
		while pos < len(text):
			while pos < len(text) and (text[pos] in node.links):
				nextn = node.links[text[pos]]
				if nextn.pattern:
					found.append((pos - len(nextn.pattern) + 1, nextn.pattern))

				outln = nextn.out
				while outln:
					found.append((pos - len(outln.pattern) + 1, outln.pattern))
					outln = outln.out

				node = node.links[text[pos]]
				pos += 1

			if node != self.root:
				node = node.fail
			else:
				pos += 1

		return found

def test():
	trie = Trie()
	for p in ["ab", "a", "abc", "bc", "c", "cba"]:
		trie.add_pattern(p)
	trie.build_links()
	print trie.search_text("abcba")

def solve_rosalind():
	pass

if __name__ == "__main__":
	test()
