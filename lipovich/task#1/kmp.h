#ifndef KMP_H_INCLUDED
#define KMP_H_INCLUDED

#include <vector>
#include <string>
#include <iostream>

typedef std::vector<int> TResult;

TResult kmp(const std::string& p, const std::string& t,  int* (*fun)(const std::string&));

#endif // KMP_H_INCLUDED
