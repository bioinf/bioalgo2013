import brute_force
import kmp_prefix
import kmp_z
import rabin_karp

import sys
import time

def main():
	if len(sys.argv) < 3:
		print "Usage:",sys.argv[0],"text pattern"
		exit()

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


	print "Brute Force ({0}):".format(s_bf),r_bf
	print "KMP-Prefix  ({0}):".format(s_kmpp),r_kmpp
	print "KMP-Z       ({0}):".format(s_kmpz),r_kmpz
	print "Rabin-Karp  ({0}):".format(s_rk),r_rk

if __name__ == "__main__":
	main()