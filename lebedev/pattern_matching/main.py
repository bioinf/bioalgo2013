# -*- coding: utf-8 -*-

import functools
import operator
import re
import time

import numpy as np

import brute_force
import kmp
import rabin_karp


def match_like_a_boss(s, p):
    n, m = len(s), len(p)
    return [offset for offset in xrange(n - m + 1) if s[offset:offset + m] == p]


def measure(f, *args, **kwargs):
    num_iter = kwargs.pop("num_iter", 1000)
    timings = []
    correct_res = match_like_a_boss(*args)
    for i in xrange(num_iter):
        tick = time.time()
        res = f(*args, **kwargs)
        timings.append((time.time() - tick) * 1000)

        if res != correct_res:
            print("{0.__module__}.{0.__name__} failed to validate! "
                  "expected: {1}, got {2}".format(f, correct_res, res))
            break
    else:
        print("mean {0:.4f}ms, sd {1:.4f}ms, median {2:.4f}ms"
              .format(np.mean(timings), np.std(timings), np.median(timings)))


def main():
    methods = [brute_force.match,
               rabin_karp.match,
               kmp.match_prefix,
               kmp.match_z]  # Stub.
    for method in methods:
        measure(method, "abacababacaaba", "aba")


if __name__ == "__main__":
    main()
