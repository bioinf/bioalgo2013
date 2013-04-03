from brute_force import brute_force as bf
from kmp_prefix import kmp_prefix as kmpp
from kmp_z import kmp_z as kmpz
from rabin_karp import rabin_karp as rk
from boyer_moore import boyer_moore as bm

import sys
import time

import random
import string

from operator import eq

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

def gettime( function, text, pattern ):
	s = time.time()
	r = function(text, pattern)
	s = time.time() - s

	return r,s

def getavgtime( function, text, pattern, n = 1000 ):
	s = sum(gettime(function, text, pattern)[1] for i in xrange(n))
	return s / n

def getrandomstring( size ):
	return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(size))

def validate():
	funcs = [bf, kmpp, kmpz, rk, bm]

	for i in xrange(10):
		text = getrandomstring(500)
		pattern = getrandomstring(10)
		if random.randint(0,1):
			pattern = text[random.randint(0,100):random.randint(100,200)]


		l = [f(text,pattern) for f in funcs]
		for i in l[1:]:
			if i != l[0]:
				return False
	return True

def main():
	if len(sys.argv) < 3:
		print "Usage:",sys.argv[0],"text pattern"
		print "Test function used"
		text,pattern = gettest()
	else:
		text    = sys.argv[1]
		pattern = sys.argv[2]

	if not validate():
		print "Some algorithms are not valid"

	print "Text:   ",text
	print "Pattern:",pattern

	s_bf = getavgtime(bf, text, pattern)
	s_kmpp = getavgtime(kmpp, text, pattern)
	s_kmpz = getavgtime(kmpz, text, pattern)
	s_rk = getavgtime(rk, text, pattern)
	s_bm = getavgtime(bm, text, pattern)	

	print "Brute Force ({0}) ".format(s_bf)
	print "KMP-Prefix  ({0}) ".format(s_kmpp)
	print "KMP-Z       ({0}) ".format(s_kmpz)
	print "Rabin-Karp  ({0}) ".format(s_rk)
	print "Boyer-Moore ({0}) ".format(s_bm)

if __name__ == "__main__":
	main()
