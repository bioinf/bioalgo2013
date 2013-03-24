# -*- coding: utf-8 -*-

def compute_prefix_function(s):
    pi = [0] * len(s)
    for offset in xrange(1, len(s)):
        i = pi[offset - 1]
        while i > 0 and s[offset] != s[i]:
            i = pi[i - 1]

        pi[offset] = i + (s[offset] == s[i])

    return pi


def compute_z_function(s):
    z = [0] * len(s)
    z[0] = len(s)
    l = r = 0
    for offset in xrange(1, len(s)):
        if offset <= r:
            z[offset] = min(z[offset - l], r - offset + 1)

        i = offset + z[offset]
        while i < len(s) and s[i] == s[i - offset]:
            i += 1

        z[offset] = i - offset
        if i - 1 > r:
            l, r = offset, i - 1

    return z


def match_prefix(s, p):
    n, m = len(s), len(p)
    if m <= n:
        pi = compute_prefix_function(p + "$" + s)
        return [i - m for i in xrange(n + 1) if pi[m + i] == m]
    else:
        return []


def match_z(s, p):
    n, m = len(s), len(p)

    if m <= n:
        z = compute_z_function(p + "$" + s)
        # Note: '+1' because of the '$' sign.
        return [i for i in xrange(n) if z[m + i + 1] == m]
    else:
        return []
