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
				
				while w != None and (sym not in w.links):
					w = w.fail

				ch_node.fail = w.links[sym] if w else self.root
				if ch_node.fail.pattern != None:
					ch_node.out = ch_node.fail
				elif ch_node.fail.out != None:
					ch_node.out = ch_node.fail.out

				queue.append(ch_node)
	
	def print_trie(self):
		queue = [self.root]

		counter = 2
		node_enum = {self.root : 1}
		while len(queue) > 0:
			node = queue.pop(0)
			for sym, ch_node in node.links.iteritems():
				if not ch_node in node_enum:
					node_enum[ch_node] = counter
					counter += 1
				print node_enum[node], node_enum[ch_node], sym
				#if ch_node.fail:
				print node_enum[ch_node], node_enum[ch_node.fail], "S"
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
	trie = Trie()
	for line in open("tr.txt", "r"):
		trie.add_pattern(line.strip("\n"))
	trie.build_links()
	trie.print_trie()

if __name__ == "__main__":
	test()
	#solve_rosalind()
