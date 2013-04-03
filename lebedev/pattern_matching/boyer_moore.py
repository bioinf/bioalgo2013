# -*- coding: utf-8 -*-

from collections import defaultdict

from kmp import compute_z_function, compute_prefix_function


def compute_bad_character(s):
    n = len(s)
    bad_character = defaultdict(int)  # ch -> last occ. of character 'ch'.
    for i in xrange(n):
        j = n - i - 1
        ch = s[j]
        bad_character[ch] = max(j, bad_character.get(ch))

    return bad_character


def compute_good_suffix(s):
    n = len(s)
    z = list(reversed(compute_z_function(s[::-1])))

    good_suffix = [0] * n
    for i in xrange(n - 1):
        if not z[i]:
            continue

        j = n - z[i]
        good_suffix[j] = i

    return good_suffix


def compute_suffix_prefix(s):
    # sp[i] is the largest suffix of s[i..n] such that it's also a
    # prefix of s.
    sp = reversed(compute_prefix_function(s[::-1]))
    return list(sp)


def match(s, p):
    def inner(offset, bad_character, good_suffix, suffix_prefix):
        """Match `s` from right to left, starting at a given `offset`."""
        for i in xrange(m):
            j = m - i - 1
            if s[offset - i] != p[j]:
                if not i:
                    return 1, False  # Special case for the 1st mismatch.
                else:
                    shift_bad_character = max(1, j - bad_character.get(p[j]))
                    shift_good_suffix = good_suffix[i] or suffix_prefix[i]
                    return max(shift_bad_character, shift_good_suffix), False

        return m - suffix_prefix[0], True

    n, m, pos = len(s), len(p), []
    if m <= n:
        pos, offset = [], m - 1
        bad_character = compute_bad_character(p)
        good_suffix = compute_good_suffix(p)
        suffix_prefix = compute_suffix_prefix(p)
        while offset < n:
            shift, matched = inner(offset, bad_character,
                                   good_suffix, suffix_prefix)
            if matched:
                pos.append(offset - m + 1)
                offset += shift
            else:
                offset += shift

    return pos
