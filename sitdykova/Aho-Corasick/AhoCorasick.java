import java.io.*;
import java.util.*;

public class AhoCorasick {

	static BufferedReader in;
	static PrintWriter out;
	static StringTokenizer st;

	static String nextToken() {
		while (st == null || !st.hasMoreTokens()) {
			try {
				st = new StringTokenizer(in.readLine());
			} catch (Exception e) {
				return "";
			}
		}
		return st.nextToken();
	}

	static int get_code(char c) {
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

	static List<List<Integer>> solve(String text, List<String> patterns) {
		int[][] trie = new int[1000001][4];
		int[] word = new int[10000001];
		Arrays.fill(word, -1);
		List<List<Integer>> ans = new ArrayList<>(patterns.size());
		for (int i = 0; i < patterns.size(); i++) {
			ans.add(new ArrayList<Integer>());
		}
		int num = 0;
		for (int i = 0; i < patterns.size(); i++) {
			String s = patterns.get(i);
			int v = 0;
			for (int j = 0; j < s.length(); j++) {
				if (trie[v][get_code(s.charAt(j))] == 0) {
					++num;
					trie[v][get_code(s.charAt(j))] = num;
				}
				v = trie[v][get_code(s.charAt(j))];
			}
			word[v] = i;
		}

		int[] fall = new int[num + 1];
		Queue<Integer> q = new LinkedList<Integer>();
		q.add(0);
		while (!q.isEmpty()) {
			int v = q.poll();
			for (int i = 0; i < 4; i++) {
				if (trie[v][i] != 0) {
					q.add(trie[v][i]);
					int w = fall[v];
					while (w > 0 && trie[w][i] == 0) {
						w = fall[w];
					}
					if (v > 0 && trie[w][i] != 0) {
						w = trie[w][i];
					}
					fall[trie[v][i]] = w;
				}
			}
		}

		int v = 0;
		for (int i = 0; i < text.length(); i++) {
			int tmp = v;
			while (v > 0 && trie[v][get_code(text.charAt(i))] == 0) {
				v = fall[v];
			}
			if (trie[v][get_code(text.charAt(i))] != 0) {
				v = trie[v][get_code(text.charAt(i))];
				trie[tmp][get_code(text.charAt(i))] = v;
				int w = v;
				while (w > 0) {
					if (word[w] != -1) {
						ans.get(word[w])
								.add(i - patterns.get(word[w]).length() + 2);
					}
					w = fall[w];
				}
			}
		}
		return ans;
	}

	public static void main(String[] args) {
		try {
			in = new BufferedReader(new FileReader("input.txt"));
			out = new PrintWriter("output.txt");
			String text = nextToken();
			List<String> patterns = new ArrayList<String>();
			String s = nextToken();
			while (s != ""){
				patterns.add(s);
				s = nextToken();
			}
			List<List<Integer>> ans = solve(text, patterns);
			for (int i = 0; i < patterns.size(); i++) {
				out.println(patterns.get(i));
				for (int pos : ans.get(i)) {
					out.print(pos + " ");
				}
				out.println();
			}
		} catch (Exception e) {
			e.printStackTrace();
			System.exit(1);
		} finally {
			out.close();
		}
	}
}