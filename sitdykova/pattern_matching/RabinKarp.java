import java.util.ArrayList;

public class RabinKarp {
	
    static int HASH_P = 5;
    static long HASH_M = 10570841 ;
    
    private String p;
    private String t;
    private long[] p_pow;

	public RabinKarp(String pattern, String text){
		p = pattern;
		t = text;
	}
	
	private long hash(String s, int s_len)
	{
	    long  res = 0;
	    for (int i = s.length() - 1; i >= 0; --i)
	        res = (res + get_code(s.charAt(s_len - i - 1)) * p_pow[i]) % HASH_M;
	    return res;
	}

	private long hash_by_prev(char c_prev, char c_cur, long hash_prev, int s_len)
	{
	    //long res = (hash_prev - (get_code(c_prev) * p_pow[s_len- 1]) * HASH_P + get_code(c_cur));
        long res = (HASH_P * hash_prev - p_pow[s_len] * get_code(c_prev) + get_code(c_cur)) % HASH_M;
        if (res < 0) res += HASH_M;
        return res;
	}

	static int get_code(char c)
	{
	    switch(c)
	    {
	        case 'A':
	          return 0;
	        case 'C':
	          return 1;
	        case 'G':
	          return 2;
	        case 'T':
	          return 3;
	        default :
	          return 0;//ololo takogo ne doljno byt'
	    }
	}
	

	public void solve() {
		int m = p.length();
		int n = t.length();
		t = t + "$";
		ArrayList<Integer> ans = new ArrayList<Integer>();
		p_pow = new long[m+1];
		p_pow[0] = 1;
		for (int i = 1; i < m+1; i++)
			p_pow[i] = (p_pow[i-1] * HASH_P) % HASH_M;
		long hp = hash(p, m);
		long h = hash(t.substring(0, m), m);

		for (int i = 0; i < n - m + 1; i++){
			if (h == hp){
				int j = 0;
				while (j < m && t.charAt(i + j) == p.charAt(j)) {
					j++;
				}
				if (j == m) {
					ans.add(i + 1);
				}
			}
			h = hash_by_prev(t.charAt(i), t.charAt(i+m), h, m);
		}
		
		/*for (int pos : ans) {
			System.out.print(pos + " ");
		}
		System.out.println();*/
	}
}
