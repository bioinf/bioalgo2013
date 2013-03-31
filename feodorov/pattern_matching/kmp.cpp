#include "algorithms.h"

std::vector<int>& get_failure_array(std::string& pattern, std::vector<int>& failure_array)
{
	int len = pattern.size();
	int i = 0, j = -1;
	failure_array.clear();
	failure_array.resize(len + 1, 0);
	failure_array[i] = j;

	while(i < len)
	{
		while(j >= 0 && pattern[i] != pattern[j])
			j = failure_array[j];
		i++, j++;
		failure_array[i] = j;
	}

	return failure_array;
}

std::vector<int>& z_function(std::string& string, std::vector<int>& z)
{
	int n = (int) string.length();
	z.resize(n, 0);

	for (int i = 1, l = 0, r = 0; i < n; ++i)
	{
		if (i <= r)
			z[i] = std::min(r - i + 1, z[i - l]);

		while (i + z[i] < n && string[z[i]] == string[i + z[i]])
			++z[i];

		if (i + z[i]-1 > r)
			l = i,  r = i + z[i] - 1;
	}
	return z;
}

std::vector<int>& KMP(std::string& sequence, std::string& pattern, std::vector<int>& res)
{
	res.clear();
	std::vector<int> failure_array;
	failure_array = get_failure_array(pattern, failure_array);

	int i = 0, j = 0;
	while (i < (int)sequence.size())
	{
		while (j >= 0 && sequence[i] != pattern[j])
			j = failure_array[j];
		i++; j++;
		if (j == (int)pattern.size())
		{
			res.push_back(i - j);
			j = failure_array[j];
		}
	}

	return res;
}

std::vector<int>& KMP_z(std::string& sequence, std::string& pattern, std::vector<int>& res)
{
	std::string str = pattern + "$" + sequence;
	std::vector<int> z;
	res.clear();

	z = z_function(str, z);
	for(unsigned int i = pattern.size() + 1; i < str.size(); ++i)
		if(z[i] == (int)pattern.size())
			res.push_back(i - pattern.size() - 1);

	return res;
}
