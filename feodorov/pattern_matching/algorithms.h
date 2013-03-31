#ifndef ALGORITHMS_H_
#define ALGORITHMS_H_

#include <string>
#include <vector>
#include <map>
#include <list>

// Task 1
std::vector<int>& brute_force(std::string& sequence, std::string& pattern, std::vector<int>& res);
std::vector<int>& KMP(std::string& sequence, std::string& pattern, std::vector<int>& res);
std::vector<int>& KMP_z(std::string& sequence, std::string& pattern, std::vector<int>& res);
std::vector<int>& rabin_karp(std::string& sequence, std::string& pattern, std::vector<int>& res);

// Task 2
std::vector<int>& boyer_moor_bad_char(std::string& text, std::string& pattern, std::vector<int>& res);
std::vector<int>& boyer_moor_good_suffix(std::string& text, std::string& pattern, std::vector<int>& res);
std::vector<int>& boyer_moor_galil(std::string& sequence, std::string& pattern, std::vector<int>& res);

#endif /* ALGORITHMS_H_ */
