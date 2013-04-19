#include "bruteforce.h"

TResult bruteforce(const std::string& p, const std::string& t)
{
    int n = p.size(), m = t.size();

    TResult res;

    for (int i = 0; i < m - n + 1; ++i)
    {
       int j = 0;

       while (j < n && p[j] == t[i + j])
       {
           ++j;
       }

       if (j == n)
       {
            res.push_back(i);
            std::cout << i << std::endl;
       }
    }

    return res;
}
