from kmp import kmp_prefix, kmp_z
from brute_force import brute_force
from rabin_karp import rabin_karp
from boyer_moore import boyer_moore
import random
import sys
import time

func = [brute_force, kmp_prefix, kmp_z, rabin_karp, boyer_moore]

def random_string(n, alphabet):
	return "".join(random.choice(alphabet) for i in xrange(n))

def test(n):
	for i in xrange(n):
		text, pattern = random_string(1000, "ACGT"), random_string(30, "ACGT")
		res = []
		for f in func:
			res.append(f(text, pattern))
		for f in res[1:]:
			if (len(f) != len(res[0])):
				print "Something is wrong"
				sys.exit(-1)
			for i in xrange(len(f)):
				if (res[0][i] != f[i]):
					print "Something is wrong"
					sys.exit(-1)
	print "OK"

def get_time(f, text, pattern):
	begin = time.time()
	f(text, pattern)
	return (time.time() - begin)

def measure(text, pattern):
	n_times = 1000
	avg_times = {}
	for f in func:
		avg_times[f.__name__] = sum(get_time(f, text, pattern) for i in range(n_times)) / n_times
	print "Text is: \n" + text
	print "Pattern is: \n" + pattern
	for (f_name, t) in avg_times.items():
		print f_name + ": " + str(t)

if (__name__ == "__main__"):
	if (len(sys.argv) == 3):
		text, pattern = sys.argv[1:]
		measure(text, pattern)
	else:
		test(1000)
