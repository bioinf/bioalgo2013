#include "algorithms.h"

std::vector<int>& rabin_karp(std::string& sequence, std::string& pattern, std::vector<int>& res)
{
	res.clear();
	const int  p = 31;
	std::vector<unsigned long long int> powers_cache(sequence.size());
	std::vector<unsigned long long int> sequence_hash(sequence.length());
	powers_cache[0] = 1;

	//calc all powers
	for (unsigned int i = 1; i < sequence.size(); ++i)
		powers_cache[i] = powers_cache[i - 1] * p;

	//calc text hash
	sequence_hash[0] = (sequence[0] - 'A' + 1) * powers_cache[0];
	for (unsigned int i = 1; i < sequence.length(); ++i)
		sequence_hash[i] = sequence_hash[i - 1] + (sequence[i] - 'A' + 1) * powers_cache[i];

	//calc pattern hash
	unsigned long long int pattern_hash = 0;
	for (unsigned int i = 0; i < pattern.length(); ++i)
		pattern_hash += (pattern[i] - 'A' + 1) * powers_cache[i];

	//find all patterns in text
	for (unsigned int i = 0; i < sequence.length() - pattern.length() + 1; ++i)
	{
		unsigned long long int hash = sequence_hash[i + pattern.length() - 1] -
				((i == 0) ? 0 : sequence_hash[i - 1]);

		if(hash == powers_cache[i] * pattern_hash)
			res.push_back(i);
	}

	return res;
}
