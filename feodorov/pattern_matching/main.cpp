#include <iostream>
#include <fstream>
#include "algorithms.h"
#include "utils.h"

int main()
{
	std::string line, sequence, pattern;

	std::ifstream input("data.txt");
	while (std::getline(input, line))
		sequence += line;
	input.close();

	input.open("pattern.txt");
	input >> pattern;
	input.close();

	std::vector<int> result;
	std::cout << sequence << std::endl << pattern << std::endl;

	std::cout << "Boyer-Moore bad char: " << std::endl;
	test(boyer_moor_bad_char, sequence, pattern, result);

	std::cout << "Boyer-Moore good suffix: " << std::endl;
	test(boyer_moor_good_suffix, sequence, pattern, result);

	std::cout << "Boyer-Moore good suffix with galil: " << std::endl;
	test(boyer_moor_galil, sequence, pattern, result);

	std::cout << "Brute force: " << std::endl;
	test(brute_force, sequence, pattern, result);

	std::cout << "KMP with failure array: " << std::endl;
	test(KMP, sequence, pattern, result);

	std::cout << "KMP with z array: " << std::endl;
	test(KMP_z, sequence, pattern, result);

	std::cout << "Rabin - Karp: " << std::endl;
	test(rabin_karp, sequence, pattern, result);

	test_correctness();
}
