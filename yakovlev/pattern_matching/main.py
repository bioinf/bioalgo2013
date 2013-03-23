import brute_force
import kmp_prefix
import kmp_z
import rabin_karp

import sys
import time

import random

def gettest():
	NUCLEO = "ACGT"

	patt_len = random.randint(0,1000)
	text_len = random.randint(0,10000)

	pattern = []
	text    = []
	for i in xrange(patt_len):
		pattern.append(NUCLEO[random.randint(0,3)])
	for i in xrange(text_len):
		text.append(NUCLEO[random.randint(0,3)])

	return "".join(text), "".join(pattern)

def main():
	if len(sys.argv) < 3:
		print "Usage:",sys.argv[0],"text pattern"
		print "Test function used"
		text,pattern = gettest()
	else:
		text    = sys.argv[1]
		pattern = sys.argv[2]

	print "Text:   ",text
	print "Pattern:",pattern

	s = time.time()
	r_bf = brute_force.brute_force(text, pattern)
	s_bf = time.time() - s

	s = time.time()
	r_kmpp = kmp_prefix.kmp_prefix(text, pattern)
	s_kmpp = time.time() - s

	s = time.time()
	r_kmpz = kmp_z.kmp_z(text, pattern)
	s_kmpz = time.time() - s

	s = time.time()
	r_rk = rabin_karp.rabin_karp(text, pattern)
	s_rk = time.time() - s

	if r_kmpp != r_bf:
		print "KMP-Prefix error!"

	if r_kmpz != r_bf:
		print "KMP-Z error!"

	if r_rk != r_bf:
		print "Rabin-Karp error!"

	print "Brute Force ({0}) ".format(s_bf)#,r_bf
	print "KMP-Prefix  ({0}) ".format(s_kmpp)#,r_kmpp
	print "KMP-Z       ({0}) ".format(s_kmpz)#,r_kmpz
	print "Rabin-Karp  ({0}) ".format(s_rk)#,r_rk

if __name__ == "__main__":
	main()
