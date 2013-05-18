#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <list>

int last_id = 1;

class Node
{
public:

	std::vector <Node *> links;
	Node * fail;
	const std::string * word;
	char label;
	int id;

	Node() : fail(NULL), id(last_id++), word(NULL) {}
	Node(char label) : 
		label(label), fail(NULL), id(last_id++), word(NULL)
	{}

	Node * next(char c)
	{
		for (size_t i = 0; i < links.size(); ++i) {
			if (links[i]->label == c) 
				return links[i];
		}
		return NULL;
	}
};

void build_trie(Node & root, const std::vector <std::string> & patterns)
{
	std::cout << "Patterns: " << std::endl;
	for (size_t i = 0; i < patterns.size(); ++i) {
		Node * curr_node = &root;
		size_t pattern_size = patterns[i].size();
		for (size_t j = 0; j < pattern_size; ++j) {
			Node * next = curr_node->next(patterns[i][j]);
			if (next == NULL) {
				Node * new_node = new Node(patterns[i][j]);
				curr_node->links.push_back(new_node);
				curr_node = new_node;
			} else {
				curr_node = next;
			}
			if (j == pattern_size - 1) {
				curr_node->word = &patterns[i];
			}
		}
		std::cout << patterns[i] << std::endl;
	}
}

void add_failures(Node & root)
{
	std::list <Node *> queue;
	queue.push_back(&root);
	root.fail = &root;
	do {
		Node * curr = queue.front();
		queue.pop_front();
		for (std::vector <Node *>::iterator it = curr->links.begin(); it != curr->links.end(); ++it) {
			if (curr != &root) {
				Node * parent = curr;
				do {
					parent = parent->fail;
					(*it)->fail = parent->next((*it)->label);
				} while(!(*it)->fail && parent != &root);
			}
			if (!(*it)->fail) {
				(*it)->fail = &root;
			}
		}
		queue.insert(queue.end(), curr->links.begin(), curr->links.end());
	} while(queue.size());
}

void print_trie(const Node & root) 
{
	std::list <const Node *> queue;
	queue.push_back(&root);
	std::cout << "Trie:" << std::endl;
	do {
		const Node * curr = queue.front();
		queue.pop_front();
		for (size_t i = 0; i < curr->links.size(); ++i) {
			std::cout << curr->id << " " << curr->links[i]->id << " " << curr->links[i]->label << std::endl;
			queue.push_back(curr->links[i]);
		}
		if (curr->fail != NULL && curr != &root) {
			std::cout << curr->id << " " << curr->fail->id << " S" << std::endl;
		}
	} while(queue.size());
}

void go(Node * &curr, char c) 
{
	while (!curr->next(c) && curr != curr->fail) {
		curr = curr->fail;
	}
	if (curr->next(c)) {
		curr = curr->next(c);
	}
}

void findMatches(const Node * node, int pos) {
	const Node * curr = node;
	while (curr->fail != curr) {
		if (curr->word) {
			std::cout << (pos - curr->word->size() + 1) << " ";
		}
		curr = curr->fail;
	}
}

void search(const std::string & text, Node & root)
{
	std::cout << "Search string: " << std::endl << text << std::endl;
	std::cout << "Results: " << std::endl;
	size_t text_len = text.size();
	Node * curr = &root;
	for (size_t i = 0; i < text_len; ++i) {
		go(curr, text[i]);
		findMatches(curr, i);
	}
}

int main(int argc, char ** argv)
{
	Node root('0');
	std::vector <std::string> patterns;
	patterns.push_back("ACGT");
	patterns.push_back("CG");
	patterns.push_back("TCG");
/*
	std::fstream fin("in");
	std::string tmp;

	while(!fin.eof()) {
		fin >> tmp;
		patterns.push_back(tmp);
	}
*/
	build_trie(root, patterns);
	add_failures(root);
	print_trie(root);

	search("GGCTCGGACGTACGCGA", root);

	std::cout << std::endl;
}
