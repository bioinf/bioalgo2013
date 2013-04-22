#ifndef KMP_H_INCLUDED
#define KMP_H_INCLUDED

#include <vector>
#include <string>
#include <iostream>

typedef std::vector<int> TResult;

int* compute_prefix_function(const std::string& s);

int* compute_z_function (const std::string& s);

TResult kmp(const std::string& p, const std::string& t,  int* (*fun)(const std::string&));

#endif // KMP_H_INCLUDED
