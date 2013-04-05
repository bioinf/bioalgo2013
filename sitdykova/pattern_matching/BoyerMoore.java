import java.util.ArrayList;

public class BoyerMoore {

	private String p;
	private String t;
	private ArrayList<Integer> ans;
	ArrayList<ArrayList<Integer>> posOfChar;

	public BoyerMoore(String pattern, String text) {
		p = pattern;
		t = text;
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

	public void solve() {
		int n = t.length();
		int m = p.length();
		ans = new ArrayList<Integer>();

		// construct "table" for bad character rule
		posOfChar = new ArrayList<>(4);
		for (int i = 0; i < 4; i++) {
			posOfChar.add(new ArrayList<Integer>());
		}
		for (int i = p.length() - 1; i >= 0; i--) {
			posOfChar.get(getCode(p.charAt(i))).add(i);
		}

		int i = 0;
		while (i < n - m + 1) {
			int j = 0;
			while (j < m && t.charAt(i + j) == p.charAt(j)) {
				j++;
			}
			if (j == m) {
				ans.add(i + 1);
				i++;
			} else {
				i += badCharacterRuleOffset(t.charAt(i + j), j);
			}
		}
		/*
		 * for (int pos : ans) { System.out.print(pos + " "); }
		 * System.out.println();
		 */
	}
}
