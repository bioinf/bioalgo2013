import java.util.ArrayList;

public class KmpPrefix  {

	private String p;
	private String t;
	private String sum;
	private int[] pref;
	
	public KmpPrefix(String pattern, String text){
		p = pattern;
		t = text;
	}

	private int building(int k, int i) {
		if (sum.charAt(i) == sum.charAt(k)) {
			return k + 1;
		}
		if (k == 0) {
			return 0;
		}
		return building(pref[k - 1], i);
	}

	public void solve() { 
		ArrayList<Integer> ans = new ArrayList<Integer>();
		sum = p + "#" + t;
		pref = new int[sum.length()];
		pref[0] = 0;
		for (int i = 1; i < sum.length(); i++) {
			pref[i] = building(pref[i - 1], i);
		}		
		for (int i = p.length(); i < sum.length(); i++) {
			if (pref[i] == p.length()) {
				ans.add(i - 2 * p.length() + 1);
			}
		}
		/*for (int pos : ans) {
			System.out.print(pos + " ");
		}
		System.out.println(); */
	}
}
