# -*- coding: utf-8 -*-

def match(s, p):
    n, m = len(s), len(p)

    pos = []
    for offset in xrange(n - m + 1):
        if all(s[offset + i] == p[i] for i in xrange(m)):
            pos.append(offset)

    return pos
