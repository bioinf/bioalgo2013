import java.util.ArrayList;

public class BruteForce  {
	private String p;
	private String t;


	public BruteForce(String pattern, String text)  {
		p = pattern;
		t = text;
	}
	
	public void solve() {
		ArrayList<Integer> ans = new ArrayList<Integer>();
		for (int i = 0; i <= t.length() - p.length(); i++) {
			int j = 0;
			while (j < p.length() && t.charAt(i + j) == p.charAt(j)) {
				j++;
			}
			if (j == p.length()) {
				ans.add(i + 1);
			}
		}
		/*for (int pos : ans) {
			System.out.print(pos + " ");
		}
		System.out.println(); */
	}
}
