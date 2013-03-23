
public class Main {
	public static void main(String[] args) {
			String pattern = args[0];
			String text = args[1];
			
		 	BruteForce brute_force = new BruteForce(pattern, text);
		 	KmpPrefix kmp_pref = new KmpPrefix(pattern, text);
		 	KmpZ kmp_z = new KmpZ(pattern, text);
		 	RabinKarp rabin_karp = new RabinKarp(pattern, text);
		 	
		 	System.out.println(pattern);
		 	System.out.println(text);
		 	
			long time = System.currentTimeMillis();
			

		 	time = System.currentTimeMillis();
		 	brute_force.solve();		 	
			System.out.println("Brute force time: " + (System.currentTimeMillis() - time));
			
			time = System.currentTimeMillis();
		 	kmp_pref.solve();
		 	System.out.println("KMP by prefix-function time: " + (System.currentTimeMillis() - time));
		 	
		 	time = System.currentTimeMillis();
		 	kmp_z.solve();
		 	System.out.println("KMP by z-function time: " + (System.currentTimeMillis() - time));
			
			time = System.currentTimeMillis();
		 	rabin_karp.solve();
		 	System.out.println("Rabin-Karp time: " + (System.currentTimeMillis() - time));

	}
}
