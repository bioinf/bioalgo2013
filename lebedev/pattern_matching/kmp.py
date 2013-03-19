# -*- coding: utf-8 -*-

def compute_prefix_function(s):
    pi = [-1] * len(s)
    pi[0] = 0

    for i in xrange(1, len(s)):
        j = pi[i - 1]
        while j > 0 and s[i] != s[j]:
            j = pi[j - 1]

        j += s[i] == s[j]
        pi[i] = j

    return pi


def match_prefix(s, p):
    n, m = len(s), len(p)
    pi = compute_prefix_function(p + "$" + s)
    return [i - m for i in xrange(n + 1) if pi[m + i] == m]


def match_z(s, p):
    pass
