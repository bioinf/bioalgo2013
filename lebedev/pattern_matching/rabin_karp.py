# -*- coding: utf-8 -*-

import sys


class rolling_hash(object):
    magic_prime = 31

    def __init__(self, s):
        self.pows = [0] * len(s)
        self.prefix_hashes = [0] * len(s)

        self.pows[0] = 1
        for i in xrange(1, len(s)):
            self.pows[i] = self.pows[i - 1] * self.magic_prime % sys.maxint

        for i, ch in enumerate(s):
            self.prefix_hashes[i] = ord(ch) * self.pows[i]
            self.prefix_hashes[i] += i and self.prefix_hashes[i - 1]
            self.prefix_hashes[i] %= sys.maxint

    def __getitem__(self, arg):
        if isinstance(arg, basestring):
            # XXX dotproduct!
            h = sum(ord(ch) * self.pows[i] for i, ch in enumerate(arg))
            return h % sys.maxint
        elif (isinstance(arg, slice) and
              not arg.step and 0 <= arg.start < arg.stop):
            i, j = arg.start, arg.stop
            h = self.prefix_hashes[j - 1]
            h -= i and self.prefix_hashes[i - 1]
            return h % sys.maxint
        else:
            raise ValueError(
                "__getitem__ should be called with a string or a slice")

    def shift(self, pattern_hash):
        return pattern_hash * self.magic_prime % sys.maxint


def match(s, p):
    n, m = len(s), len(p)
    pos = []

    if m <= n:
        rh = rolling_hash(s)
        pattern_hash = rh[p]
        for offset in xrange(n - m + 1):
            if (rh[offset:offset + m] == pattern_hash and
                all(s[offset + i] == p[i] for i in xrange(m))):
                pos.append(offset)

            pattern_hash = rh.shift(pattern_hash)

    return pos
