# -*- coding: utf-8 -*-

import time
import random
import numpy as np


from kmp import *
from bruteforce import *
from rabin_karp import *

def measure_time(f, *args):
    num_iter = 1000
    timings = np.zeros(num_iter)

    for i in xrange(num_iter):
        start = time.time()
        f(*args)
        timings[i] = (time.time() - start)*1e6

    q1 = np.percentile(timings, 25)
    q3 = np.percentile(timings, 75)
    iqr = q3 - q1
    lo_extreme = q1 - 3 * iqr
    hi_extreme = q3 + 3 * iqr

    mask = np.logical_and(timings >= lo_extreme, timings <= hi_extreme)
    solid = timings[mask]
    return "{0}:\nmean is {1} us ({2} solid timings, {3} outliers)".format(f.__name__, solid.mean(), len(solid), num_iter - len(solid))

alphabet = 'abcdefgh'

string_random = ''.join([random.choice(alphabet) for i in xrange(3000)])
sub_random = 'abdf'

string_oneletter = 'a'*3000
sub_oneletter = 'aaaa'

string_lastletter = 'a'*2999 + 'b'
sub_lastletter = 'aaab'

string_pattern = 'ab'*1500
sub_pattern = 'baba'


functions = [brute_force, kmp_prefix, kmp_z, rabin_karp]

def output(descr, functionname, string, sub):
    results.write("\n\n{0} results for {1}:\nstring: {2}...{3}\nsubstring: {4}\n\n".format(descr, functionname, string[:7], string[-4:], sub))
    for f in functions:
        results.write(measure_time(f, string, sub) + '\n')

with open('results.txt', 'w') as results:
    output('Best', 'brute-force', string_random, sub_random)
    output('Worse', 'brute-force', string_lastletter, sub_lastletter)

    output('Best', 'Rabin-Karp', string_lastletter, sub_lastletter)
    output('Worse', 'Rabin-Karp', string_pattern, sub_pattern)

    output('Best', 'KMP', string_oneletter, sub_oneletter)