
public class Main {
	public static void main(String[] args) {
			String pattern = args[0];
			String text = args[1];
			int n = 100;
			long time;
			double[] results = new double[4];
			
		 	BruteForce brute_force = new BruteForce(pattern, text);
		 	KmpPrefix kmp_pref = new KmpPrefix(pattern, text);
		 	KmpZ kmp_z = new KmpZ(pattern, text);
		 	RabinKarp rabin_karp = new RabinKarp(pattern, text);
		 	
		 	System.out.println(pattern);
		 	System.out.println(text);
			
			for (int i = 0; i < n; i++){
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
		 	
			}
			System.out.println("Brute force time: " + (results[0]/n));
			System.out.println("KMP by prefix-function time: " + (results[1]/n));
			System.out.println("KMP by z-function time: " + (results[2]/n));
			System.out.println("Rabin-Karp time: " + (results[3]/n));
	}
}