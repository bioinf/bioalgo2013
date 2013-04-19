#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <time.h>

#include "kmp.h"
#include "bruteforce.h"
#include "rabin_carp.h"

std::ifstream ifs("gen.txt", std::ios::in);
std::ofstream ofs("out.txt", std::ios::trunc);

using std::string;

const int max_disp_length = 1000;

void log_res(const std::string alg, const std::string& p, const std::string& t, double time, TResult& res)
{
    ofs << alg << " method:" << std::endl << std::endl;

    if (t.length() <= max_disp_length)
    {
        ofs << p << std::endl << t << std::endl;
    }
    else
    {
        ofs << "Text too long for display..." << std::endl;
    }

    ofs << std::endl << "Pattern matching positions in text:" << std::endl;

    for (int i = 0; i < res.size(); ++i)
    {
        ofs << res[i] << " ";
    }

    ofs.precision(5);

    ofs << std::endl << "Computation time: " << time << std::endl << std::endl;

}

int* compute_prefix_function(const string& s)
{
    int len = (int) s.length();

    int* p = new int[len];

    for (int i = 0; i < len; ++i)
	{
	    p[i] = 0;
	}

    p[0] = 0;
    int k = 0;

    for(int i = 1; i < len; i++)
    {
            while (k > 0  && s[k] != s[i])
            {
                k = p[k-1];
            }

            if (s[k] == s[i])
            {
                k++;
            }

            p[i] = k;
    }

    return p;
}

int* compute_z_function (const string& s)
{
	int n = (int) s.length();

	int* z = new int[n];

	for (int i = 0; i < n; ++i)
	{
	    z[i] = 0;
	}

	for (int i = 1, l = 0, r = 0; i < n; ++i)
	{
		if (i <= r)
		{
		    z[i] = std::min(r - i + 1, z[i - l]);
		}

		while (i + z[i] < n && s[z[i]] == s[i + z[i]])
		{
		    ++z[i];
		}

		if (i + z[i] - 1 > r)
		{
		   l = i, r = i + z[i] - 1;
		}
	}

	return z;
}

int main()
{

    string p, t;

    ifs >> p >> t;

    int* (*fptr)(const string&);
//
    clock_t begin, end;
//
    begin = clock();

    TResult brut = bruteforce(p, t);

    end = clock();

    double diff0 = (double(end) - double(begin)) / CLOCKS_PER_SEC;

    log_res("Bruteforce", p, t, diff0, brut);

    std::cout << "bruteforced" << " " << diff0 << std::endl;


    //////////////////////

    begin = clock();

    fptr = compute_z_function;

    TResult kmpz = kmp(p, t, fptr);

    end = clock();

    double diff1 = (double(end) - double(begin)) / CLOCKS_PER_SEC;

    log_res("KMP with z-function", p, t, diff1, kmpz);

    std::cout << "kmpz" << " " << diff1 << std::endl;

    //////////////////////

    begin = clock();

    fptr = compute_prefix_function;

    TResult kmpp = kmp(p, t, fptr);

    end = clock();

    double diff2 =(double(end) - double(begin)) / CLOCKS_PER_SEC;

    log_res("KMP with prefix-function", p, t, diff2, kmpp);

    std::cout << "kmpp" << std::endl;

    //////////////////////


    begin = clock();

    TResult rc = rabin_carp(p, t);

    end = clock();

    double diff3 = (double(end) - double(begin)) / CLOCKS_PER_SEC;

    log_res("Rabin-Carp", p, t, diff3, rc);

    std::cout << "rc" << std::endl;

    return 0;
}
