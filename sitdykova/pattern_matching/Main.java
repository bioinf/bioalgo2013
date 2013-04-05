public class Main {
	public static void main(String[] args) {
		String pattern = args[0];
		String text = args[1];
		//int n = 100;
		int n = 1;
		long time;
		double[] results = new double[5];

		BruteForce brute_force = new BruteForce(pattern, text);
		KmpPrefix kmp_pref = new KmpPrefix(pattern, text);
		KmpZ kmp_z = new KmpZ(pattern, text);
		RabinKarp rabin_karp = new RabinKarp(pattern, text);
		BoyerMoore boyer_moore = new BoyerMoore(pattern, text);

		System.out.println(pattern);
		System.out.println(text);
		try {
			for (int i = 0; i < n; i++) {
				time = System.currentTimeMillis();
				brute_force.solve();
				results[0] += (System.currentTimeMillis() - time);

				time = System.currentTimeMillis();
				kmp_pref.solve();
				results[1] += (System.currentTimeMillis() - time);

				time = System.currentTimeMillis();
				kmp_z.solve();
				results[2] += (System.currentTimeMillis() - time);

				time = System.currentTimeMillis();
				rabin_karp.solve();
				results[3] += (System.currentTimeMillis() - time);

				time = System.currentTimeMillis();
				boyer_moore.solve();
				results[4] += (System.currentTimeMillis() - time);
			}
			System.out.println("Brute force time: " + (results[0] / n));
			System.out.println("KMP by prefix-function time: "
					+ (results[1] / n));
			System.out.println("KMP by z-function time: " + (results[2] / n));
			System.out.println("Rabin-Karp time: " + (results[3] / n));
			System.out.println("Boyer-Moore time: " + (results[4] / n));
		} catch (IllegalStateException e) {
			System.out.println(e);
		}
	}
}