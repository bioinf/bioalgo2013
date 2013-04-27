import java.io.*;
import java.util.Scanner;

public class local implements Runnable {
	public static void main(String[] args) {
		new Thread(new local()).start();
	}

	Scanner in;
	Scanner pam250;
	PrintWriter out;
	int[][] s;
	int gap_penalty = 5;

	@Override
	public void run() {
		try {
			in = new Scanner(new File("rosalind_loca.txt"));
			pam250 = new Scanner(new File("pam250.txt"));
			out = new PrintWriter("output.txt");
			solve();
		} catch (FileNotFoundException e) {
			e.printStackTrace();
			System.exit(1);
		} finally {
			out.close();
		}
	}

	int getCode(char c) {
		int code = c - 'A';
		if (code == 0)
			return 0;
		if (code < 9)
			return code - 1;
		if (code < 14)
			return code - 2;
		if (code < 20)
			return code - 3;
		if (code < 23)
			return code - 4;
		return 19;
	}

	int max(int a, int b, int c, int d) {
		return Math.max(Math.max(a, b), Math.max(c, d));
	}

	void solve() {
		s = new int[20][20];
		for (int i = 0; i < 20; i++) {
			for (int j = 0; j < 20; j++) {
				s[i][j] = pam250.nextInt();
			}
		}

		String a = "";
		in.next();
		String next = in.next();
		while (next.charAt(0) != '>') {
			a += next;
			next = in.next();
		}
		int n = a.length() + 1;
		String b = "";
		while (in.hasNext()) {
			b += in.next();
		}
		int m = b.length() + 1;

		int maxScore = 0;
		int maxi = 0;
		int maxj = 0;

		int[][] score = new int[n][m];
		for (int i = 1; i < n; i++) {
			for (int j = 1; j < m; j++) {
				score[i][j] = max(
						0,
						score[i - 1][j] - gap_penalty,
						score[i][j - 1] - gap_penalty,
						score[i - 1][j - 1]
								+ s[getCode(a.charAt(i - 1))][getCode(b
										.charAt(j - 1))]);
				if (score[i][j] > maxScore) {
					maxScore = score[i][j];
					maxi = i;
					maxj = j;
				}
			}
		}
		out.println(maxScore);
		String s = "";
		String p = "";
		while (maxScore != 0) {
			if (maxScore == score[maxi - 1][maxj] - gap_penalty) {
				s = a.charAt(maxi - 1) + s;
				maxScore = score[maxi - 1][maxj];
				maxi--;
			} else {
				if (maxScore == score[maxi][maxj - 1] - gap_penalty) {
					p = b.charAt(maxj - 1) + p;
					maxScore = score[maxi][maxj - 1];
					maxj--;
				} else {
					s = a.charAt(maxi - 1) + s;
					p = b.charAt(maxj - 1) + p;
					maxScore = score[maxi - 1][maxj - 1];
					maxi--;
					maxj--;
				}
			}
		}
		out.println(s);
		out.println(p);
	}
}