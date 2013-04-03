# -*- coding: utf-8 -*-

from __future__ import print_function

import functools
import operator
import random
import re
import string
import sys
import time

try:
    import numpy as np
except ImportError:
    import numpypy as np

    np.median = lambda xs: list(sorted(xs))[len(xs) / 2]

import brute_force
import kmp
import rabin_karp
import boyer_moore


def match_like_a_boss(s, p):
    n, m = len(s), len(p)
    return [offset for offset in xrange(n - m + 1) if s[offset:offset + m] == p]


def measure(f, s, p, num_iter=1000):
    name = "{0.__module__}.{0.__name__}".format(f)
    timings = []
    correct_res = match_like_a_boss(s, p)
    for i in xrange(num_iter):
        tick = time.time()
        res = f(s, p)
        timings.append((time.time() - tick) * 1000)

        if res != correct_res:
            print("{0:20} failed to validate! expected: {1}, got {2}"
                  .format(name, correct_res, res))
            sys.exit(1)
    else:
        print("{0:20} mean {1:.4f}ms, sd {2:.4f}ms, median {3:.4f}ms"
              .format(name, np.mean(timings), np.std(timings),
                      np.median(timings)))

def measure_all(s, p):
    methods = [brute_force.match,
               rabin_karp.match,
               kmp.match_prefix,
               kmp.match_z,
               boyer_moore.match]

    print("T = {0!r}\nP = {1!r}".format(s, p))
    for method in methods:
        measure(method, s, p)
    print()


def main():
    def periodic_string(s, n):
        return s * n

    def random_string(n, alphabet=string.letters):
        n = random.randint(1, n)
        return "".join(random.choice(alphabet) for _ in xrange(n))

    # Trivial.
    measure_all("abacababacaaba", "aba")

    # Fuzz.
    for _ in xrange(10):
        measure_all(random_string(64, "ab"), periodic_string(16, "ab"))
        measure_all(random_string(16, "ab"), random_string(64, "ab"))
        measure_all(random_string(256), random_string(64))

    measure_all(periodic_string("a", 256), periodic_string("a", 255))
    measure_all(periodic_string("abba", 256), periodic_string("abba", 255))


if __name__ == "__main__":
    main()
