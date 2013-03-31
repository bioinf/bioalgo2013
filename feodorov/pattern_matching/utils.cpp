#include <iostream>
#include <ctime>
#include <cstdlib>
#include "algorithms.h"
#include "utils.h"

void print_map_of_lists(const std::map<char, std::list<int> >& data)
{
	for(std::map<char, std::list<int> >::const_iterator it = data.begin(); it != data.end(); ++it)
	{
		std::cout << it->first << ": ";
		for(std::list<int>::const_iterator iter = it->second.begin(); iter != it->second.end(); ++iter)
		{
			std::cout << *iter << " ";
		}
		std::cout << std::endl;
	}
}

void print_vector(const std::vector<int>& res)
{
	for(unsigned int i = 0; i < res.size(); ++i)
		std::cout << res[i] << "\t";
	std::cout << std::endl;
}

std::string generate_random_string(int size)
{
	std::vector<char> str;
	for(int i = 0; i < size; ++i)
	{
		switch((int)rand() % 4)
		{
			case 0:
				str.push_back('A');
				break;
			case 1:
				str.push_back('C');
				break;
			case 2:
				str.push_back('G');
				break;
			case 3:
				str.push_back('T');
				break;
		}
	}
	return std::string(str.begin(), str.end());
}


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

		std::vector<int> bruteforce_res, kmp_prefix_res, kmp_z_res, rk_z_res, bm_bchar_res, bm_gsuff_res, bm_galil_res;
		brute_force(text, pattern, bruteforce_res);
		KMP(text, pattern, kmp_prefix_res);
		KMP_z(text, pattern, kmp_z_res);
		rabin_karp(text, pattern, rk_z_res);
		boyer_moor_bad_char(text, pattern, bm_bchar_res);
		boyer_moor_good_suffix(text, pattern, bm_gsuff_res);
		boyer_moor_galil(text, pattern, bm_galil_res);

		for(int i = 0; i < (int)kmp_z_res.size(); ++i)
		{
			if(bruteforce_res[i] != kmp_prefix_res[i] || kmp_z_res[i] != rk_z_res[i] ||
					bruteforce_res[i] != kmp_z_res[i] || kmp_prefix_res[i] != rk_z_res[i] ||
					bm_bchar_res[i] != bruteforce_res[i] || bm_gsuff_res[i] != bruteforce_res[i] ||
					bm_galil_res[i] != bruteforce_res[i])
			{
				std::cout << "brute force: " << bruteforce_res[i] << std::endl;
				std::cout << "kmp_prefix_res: " << kmp_prefix_res[i] << std::endl;
				std::cout << "kmp_z_res: " << kmp_z_res[i] << std::endl;
				std::cout << "rk_z_res: " << rk_z_res[i] << std::endl;
				std::cout << "bm_bchar_res: " << bm_bchar_res[i] << std::endl;
				std::cout << "bm_gsuff_res: " << bm_gsuff_res[i] << std::endl;
				std::cout << "bm_galil_res: " << bm_galil_res[i] << std::endl;
				std::cout << "Error for pattern " << pattern << " in " << text << std::endl;
			}
		}
	}
	std::cout << "Passed" << std::endl;
}

