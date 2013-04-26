import java.util.ArrayList;

public class BoyerMoore {

	private String p, t;
	private int m, n;
	private List<Integer> ans;
	List<List<Integer>> posOfChar;
	int[] L, l;

	public BoyerMoore(String pattern, String text) {
		p = pattern;
		t = text;
		m = p.length();
		n = t.length();
	}

	private static int getCode(char c) {
		switch (c) {
		case 'A':
			return 0;
		case 'C':
			return 1;
		case 'G':
			return 2;
		case 'T':
			return 3;
		default:
			throw new IllegalStateException("ololo, it's not DNA");
		}
	}

	private int badCharacterRuleOffset(char c, int j) {
		int i = 0;
		int charIndex = getCode(c);
		int lolo = posOfChar.get(charIndex).size();
		while (i < lolo && posOfChar.get(charIndex).get(i) > j) {
			i++;
		}
		if (i == posOfChar.get(charIndex).size()) {
			return j + 1;
		} else {
			return j - posOfChar.get(charIndex).get(i);
		}
	}

	private int goodSuffixRuleOffset(int j) {
		if (j == m)
			return 1;
		if (L[j] > 0) {
			return m - L[j] - 1;
		} else {
			return m - l[j];
		}
	}

	private int[] zFunction(String s) {
		int[] z = new int[s.length()];
		int left = 0;
		int right = 0;
		for (int i = 1; i < s.length(); i++) {
			if (i > right) {
				int j = 0;
				while (j + i < s.length() && s.charAt(i + j) == s.charAt(j)) {
					j++;
				}
				z[i] = j;
				left = i;
				right = i + j - 1;
			} else if (z[i - left] >= right - i + 1) {
				int j = 1;
				while (j + right < s.length()
						&& s.charAt(right + j) == s.charAt(right - i + j)) {
					j++;
				}
				z[i] = right - i + j;
				left = i;
				right += j - 1;
			} else {
				z[i] = z[i - left];
			}
		}
		return z;
	}

	public void solve() {
		ans = new ArrayList<Integer>();

		// construct "table" for bad character rule
		posOfChar = new ArrayList<>(4);
		for (int i = 0; i < 4; i++) {
			posOfChar.add(new ArrayList<Integer>());
		}
		for (int i = p.length() - 1; i >= 0; i--) {
			posOfChar.get(getCode(p.charAt(i))).add(i);
		}

		// construct table for good suffix rule
		String rev_p = new StringBuilder(p).reverse().toString();
		int[] rev_z = zFunction(rev_p);
		// n[j] == rev_z[m - j - 1]
		L = new int[m + 1];
		for (int j = 1; j < m - 2; j++) {
			int i = m - rev_z[m - j - 1];
			L[i] = j;
		}
		l = zFunction(p);
		for (int j = m - 2; j >= 0; j--) {
			if (l[j] < m - j)
				l[j] = l[j + 1];
		}

		int i = m - 1;
		while (i < n) {
			int j = m - 1;
			int k = i;
			while (j >= 0 && t.charAt(k) == p.charAt(j)) {
				j--;
				k--;
			}
			if (j < 0) {
				ans.add(i - m + 2);
				i += m - l[1]; // Galil's rule
			} else {
				i += Math.max(badCharacterRuleOffset(t.charAt(k), j),
						goodSuffixRuleOffset(j + 1));
			}
		}

		/*
		 * for (int pos : ans) { System.out.print(pos + " "); }
		 * System.out.println();
		 */

	}
}
