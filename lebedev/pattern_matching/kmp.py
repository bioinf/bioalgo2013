# -*- coding: utf-8 -*-

def compute_prefix_function(s):
    pi = [0] * len(s)
    for offset in xrange(1, len(s)):
        i = pi[offset - 1]
        while i > 0 and s[offset] != s[i]:
            i = pi[i - 1]

        pi[i] = i + (s[offset] == s[i])

    return pi


def compute_z_function(s):
    n = len(s)
    z = [0] * n
    for offset in xrange(n):
        i = offset
        while i < n and s[i - offset] == s[i]:
            z[offset] += 1
            i += 1

    return z


def match_prefix(s, p):
    n, m = len(s), len(p)
    pi = compute_prefix_function(p + "$" + s)
    return [i - m for i in xrange(n + 1) if pi[m + i] == m]


def match_z(s, p):
    n, m = len(s), len(p)
    z = compute_z_function(p + "$" + s)
    # Note: '+1' because of the '$' sign.
    return [i for i in xrange(n) if z[m + i + 1] == m]
