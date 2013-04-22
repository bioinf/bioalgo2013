#include "kmp.h"

int* compute_prefix_function(const std::string& s)
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

int* compute_z_function (const std::string& s)
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
