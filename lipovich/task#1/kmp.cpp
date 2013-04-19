#include "kmp.h"


TResult kmp(const std::string& p, const std::string& t,  int* (*fun)(const std::string&))
{
    int* f_array = fun(p);

    TResult res;

    int n = p.size(), m = t.size();

    int i = 0, j = 0;

    for (i, j; i + j < m; j = f_array[j], ++i)
    {
        while (j < n && p[j] == t[i + j])
        {
            ++j;
        }

        if (j == n)
        {
            res.push_back(i);
            --j;
        }
    }

    delete f_array;

    return res;
}
