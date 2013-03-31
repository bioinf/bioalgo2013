#ifndef UTILS_H_
#define UTILS_H_

#include <string>
#include <vector>
#include <map>
#include <list>

//debug functions
void print_map_of_lists(const std::map<char, std::list<int> >& data);
void print_vector(const std::vector<int>& res);

//test functions
typedef std::vector<int>& (*func_t)(std::string& sequence, std::string& pattern, std::vector<int>& res);
std::string generate_random_string(int size);
void test(func_t func, std::string& sequence, std::string& pattern, std::vector<int>& res);
void test_correctness();

#endif /* UTILS_H_ */
