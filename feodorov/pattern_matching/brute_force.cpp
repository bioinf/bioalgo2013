#include "algorithms.h"

std::vector<int>& brute_force(std::string& sequence, std::string& pattern, std::vector<int>& res)
{
	res.clear();

	for(unsigned int i = 0; i < sequence.size() - pattern.size() + 1; ++i)
	{
		bool is_match = true;
		for(unsigned int j = 0; j < pattern.size(); ++j)
			if(sequence[i + j] != pattern[j])
			{
				is_match = false;
				continue;
			}

		if(is_match)
			res.push_back(i);
	}

	return res;
}
