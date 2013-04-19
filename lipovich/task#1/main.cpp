#include <iostream>
#include <vector>
#include <string>
#include <fstream>

#include "kmp.h"
#include "bruteforce.h"
#include "rabin_carp.h"
#include "log.h"

std::ifstream ifs("gen.txt", std::ios::in);
std::ofstream ofs("out.txt", std::ios::trunc);

using std::string;

float time_diff(timespec _beg, timespec _end)
{
    return (_end.tv_nsec - _beg.tv_nsec)/1e9f;
}

int main()
{

    string p, t;

    ifs >> p >> t;

    int* (*fptr)(const string&);

    timespec begin, end;

    clock_gettime(CLOCK_REALTIME, &begin);

    TResult brut = bruteforce(p, t);

    clock_gettime(CLOCK_REALTIME, &end);

    log_res("Bruteforce", p, t, time_diff(begin, end), brut);

    //////////////////////

    clock_gettime(CLOCK_REALTIME, &begin);

    fptr = compute_z_function;

    TResult kmpz = kmp(p, t, fptr);

    clock_gettime(CLOCK_REALTIME, &end);

    log_res("KMP with z-function", p, t, time_diff(begin, end), kmpz);

    //////////////////////

    clock_gettime(CLOCK_REALTIME, &begin);

    fptr = compute_prefix_function;

    TResult kmpp = kmp(p, t, fptr);

    clock_gettime(CLOCK_REALTIME, &end);

    log_res("KMP with prefix-function", p, t, time_diff(begin, end), kmpp);

    //////////////////////


    clock_gettime(CLOCK_REALTIME, &begin);

    TResult rc = rabin_carp(p, t);

    clock_gettime(CLOCK_REALTIME, &end);

    log_res("Rabin-Carp", p, t, time_diff(begin, end), rc);

    return 0;
}
