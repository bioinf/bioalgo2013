#ifndef RABIN_CARP_H_INCLUDED
#define RABIN_CARP_H_INCLUDED
#include <vector>
#include <string>
#include <iostream>

typedef std::vector<int> TResult;

const unsigned int a = 2;

TResult rabin_carp(const std::string& p, const std::string& t);

#endif // RABIN_CARP_H_INCLUDED
