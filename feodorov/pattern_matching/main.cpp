#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <ctime>
#include <cstdlib>

void print_vector(std::vector<int>& res)
{
	for(unsigned int i = 0; i < res.size(); ++i)
		std::cout << res[i] << "\t";
	std::cout << std::endl;
}

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
	while (i < sequence.size())
	{
		while (j >= 0 && sequence[i] != pattern[j])
			j = failure_array[j];
		i++; j++;
		if (j == pattern.size())
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
		if(z[i] == pattern.size())
			res.push_back(i - pattern.size() - 1);

	return res;
}

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
std::string generate_random_string(int size)
{
	std::vector<char> str;
	for(int i = 0; i < size; ++i)
	{
		switch((int)rand() % 4)
		{
			case 1:
				str.push_back('A');
			case 2:
				str.push_back('C');
			case 3:
				str.push_back('G');
			case 4:
				str.push_back('T');
		}
	}
	return std::string(str.begin(), str.end());
}

typedef std::vector<int>& (*func_t)(std::string& sequence, std::string& pattern, std::vector<int>& res);

void test(func_t func, std::string& sequence, std::string& pattern, std::vector<int>& res)
{
	clock_t start = clock();
	for(int i = 0; i < 10000; ++i)
		func(sequence, pattern, res);
	clock_t ends = clock();
	std::cout << "Running Time : " << (double) (ends - start) / CLOCKS_PER_SEC << std::endl;
}

void test_correctness()
{
	std::cout << "Correctness test" << std::endl;
	for(int i = 0; i < 100; ++i)
	{
		std::string pattern = generate_random_string(5);
		std::string text = generate_random_string(50);

		std::vector<int> bruteforce_res, kmp_prefix_res, kmp_z_res, rk_z_res;
		brute_force(text, pattern, bruteforce_res);
		KMP(text, pattern, kmp_prefix_res);
		KMP_z(text, pattern, kmp_z_res);
		rabin_karp(text, pattern, rk_z_res);
		for(int i = 0; i < kmp_z_res.size(); ++i)
		{
			if(bruteforce_res[i] != kmp_prefix_res[i] || kmp_z_res[i] != rk_z_res[i] ||
					bruteforce_res[i] != kmp_z_res[i] || kmp_prefix_res[i] != rk_z_res[i])
			{
				std::cout << "bruteforce: " << bruteforce_res[i] << std::endl;
				std::cout << "kmp_prefix_res: " << kmp_prefix_res[i] << std::endl;
				std::cout << "kmp_z_res: " << kmp_z_res[i] << std::endl;
				std::cout << "rk_z_res: " << rk_z_res[i] << std::endl;
				std::cout << "Error for pattern " << pattern << " in " << text << std::endl;
			}
		}
	}
	std::cout << "Passed" << std::endl;
}

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
