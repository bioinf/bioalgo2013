import java.util.ArrayList;

public class KmpZ {
	
	private String p;
	private String t;
	
	public KmpZ(String pattern, String text){
		p = pattern;
		t = text;
	}

	public void solve() {
		ArrayList<Integer> ans = new ArrayList<Integer>();
		String sum = p + "#" + t;
		int[] z = new int[sum.length()];
		int left = 0;
		int right = 0;
		for (int i = 1; i < sum.length(); i++) {
			if (i > right) {
				int j = 0;
				while (j + i < sum.length() && sum.charAt(i + j) == sum.charAt(j)) {
					j++;
				}
				z[i] = j;
				left = i;
				right = i + j - 1;
			} else if (z[i - left] >= right - i + 1) {
				int j = 1;
				while (j + right < sum.length()
						&& sum.charAt(right + j) == sum.charAt(right - i + j)) {
					j++;
				}
				z[i] = right - i + j;
				left = i;
				right += j - 1;
			} else {
				z[i] = z[i - left];
			}
		}

		for (int i = p.length(); i < sum.length(); i++) {
			if (z[i] == p.length()) {
				ans.add(i - p.length());
			}
		}
		/*for (int pos : ans) {
			System.out.print(pos + " ");
		}
		System.out.println();*/
	}
}
