#!/usr/bin/env python2

import random
import time
import numpy as np
import algorithms as alg
import boyer_moore as bm
import string

def measure(f, *args):
	num_iter = 1000
	timings = np.zeros(num_iter)

	for i in xrange(num_iter):
		tick = time.time()
		res = f(*args)  # Execute f.
		timings[i] = (time.time() - tick) * 1e6

		# Optionally check if ``res`` is correct.

	q1 = np.percentile(timings, 25)
	q3 = np.percentile(timings, 75)
	iqr = q3 - q1
	lo_extreme = q1 - 3 * iqr
	hi_extreme = q3 + 3 * iqr

	# Filter outliers and print mean execution time. See link for details:
	# http://www.itl.nist.gov/div898/handbook/prc/section1/prc16.htm
	mask = np.logical_and(timings >= lo_extreme, timings <= hi_extreme)
	solid = timings[mask]
	#print("mean is {0} us ({1} solid timings, {2} outliers)"
	#      .format(solid.mean(), len(solid), num_iter - len(solid)))
	return solid.mean()

def check_fail():
	fail_flag = False
	for i in xrange(100):
		text = "".join(random.choice("ACGT") for i in xrange(100))
		pattern = "".join(random.choice("ACGT") for i in xrange(6))
		if not (alg.kmp(text, pattern) == 
				alg.karp(text, pattern) == 
				alg.naive(text, pattern) == 
				alg.z_find(text, pattern) ==
				bm.boyer_moore(text, pattern)):
			print alg.naive(text, pattern), bm.boyer_moore(text, pattern)
			fail_flag = True

	if fail_flag:
		return "Fail!"
	else:
		return "Not fail!"

def union_find(text, pattern):
	print "Pattern: {0}\nText: {1}\n".format(pattern, text)
	print ("Running time: \nNaive: {0}\nKMP: {1}\nZ-function: {2}\nRabin-Karp: {3}\nBoyer-Moore: {4}\n"
			.format(measure(alg.naive, text, pattern), measure(alg.kmp, text, pattern),
					measure(alg.z_find, text, pattern), measure(alg.karp, text, pattern),
					measure(bm.boyer_moore, text, pattern)))

def main():
	print "=================\nKMP is best:\n==============="
	union_find("ACCCGGGCCTAGGACAAGGAACCTTTGGAGGAGGCTTAGCCGCCCCCTTAGAGGACCAT", "CCTAA")
	print "=================\nRabin-Karp is best\n========="
	union_find("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab", "aaaaaaaaa")
	print "=================\nNaive is best:\n============="
	union_find("abcdefghjklmnopqrstuvwxyz", "wwwwwwww")

	print check_fail()


if __name__ == "__main__":
	main()
