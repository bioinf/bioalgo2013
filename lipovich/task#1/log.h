#ifndef LOG_H_INCLUDED
#define LOG_H_INCLUDED
#include <string>
#include <vector>
#include <fstream>

const int max_disp_length = 1000;

typedef std::vector<int> TResult;

void log_res(const std::string alg, const std::string& p, const std::string& t, double time, TResult& res);

#endif // LOG_H_INCLUDED
