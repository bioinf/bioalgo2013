from kmp import kmp_prefix, kmp_z
from brute_force import brute_force
import random
import sys

def random_string(n, alphabet):
	return "".join(random.choice(alphabet) for i in xrange(n))

def test(n):
	for i in xrange(n):
		text, pattern = random_string(1000, "ACGT"), random_string(30, "ACGT")
		bf = brute_force(text, pattern)
		kmp_pr = kmp_prefix(text, pattern)
		kmp_zr = kmp_z(text, pattern)
		if (len(bf) != len(kmp_pr) or len(bf) != len(kmp_zr)):
			print "BF " + str(bf)
			print "kmp pref " + str(kmp_pr)
			print "kmp z " + str(kmp_zr)
			sys.exit(-1)
		for i in xrange(len(bf)):
			if (bf[i] != kmp_pr[i] or bf[i] != kmp_zr[i]):
				print "BF " + str(bf)
				print "kmp pref " + str(kmp_pr)
				print "kmp z " + str(kmp_zr)
				sys.exit(-1)
	print "OK"

if (__name__ == "__main__"):
	if (len(sys.argv) != 1):
		text, pattern = sys.argv[1:]
	else:
		text, pattern = random_string(1000, "ACGT"), random_string(30, "ACGT")
	test(1000)
