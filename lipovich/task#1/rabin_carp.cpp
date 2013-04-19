#include "rabin_carp.h"

bool check(const std::string& p, const std::string& t, int pos, int n)
{
    for (int i = pos; i < pos + n; ++i)
    {
        if (p[i - pos] != t[i])
        {
            return false;
        }
    }
    return true;
}

TResult rabin_carp(const std::string& p, const std::string& t)
{
    int n = p.size(), m = t.size();

    long long hash_p = 0, hash_t = 0, g = 1;

    TResult res;

    //Calc initial hash of pattern and text
    for (int i = 0; i < n; ++i)
    {
        hash_p = (a * hash_p + (int)p[i]) % 31;

        hash_t = (a * hash_t + (int)t[i]) % 31;

        g = (a * g) % 31;
    }

    for (int i = 0; i < m - n + 1; ++i)
    {

        if (hash_p == hash_t && check(p, t, i, n))
        {
            res.push_back(i);
        }

        hash_t = (a * hash_t - (g * (int)t[i]) % 31 + (int)t[i + n]) % 31;
    }

    return res;
}




