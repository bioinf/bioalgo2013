import java.io.*;
import java.util.Scanner;

public class global implements Runnable {
	public static void main(String[] args) {
		new Thread(new global()).start();
	}

	Scanner in;
	Scanner blosum62;
	PrintWriter out;
	int[][] s;
	int gap_penalty = 5;

	@Override
	public void run() {
		try {
			in = new Scanner(new File("rosalind_glob.txt"));
			blosum62 = new Scanner(new File("blosum62.txt"));
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

	int max(int a, int b, int c) {
		return Math.max(Math.max(a, b), Math.max(b, c));
	}

	void solve() {
		s = new int[20][20];
		for (int i = 0; i < 20; i++) {
			for (int j = 0; j < 20; j++) {
				s[i][j] = blosum62.nextInt();
			}
		}

		String a = "";
		in.next();
		String next = in.next();
		while (next.charAt(0) != '>'){
			a += next;
			next = in.next();
		}
		int n = a.length() + 1;
		String b = "";
		while (in.hasNext()){
			b += in.next();
		}
		int m = b.length() + 1;

		int[][] score = new int[n][m];
		for (int j = 0; j < m; j++) {
			score[0][j] = -gap_penalty * j;
		}
		for (int i = 0; i < n; i++) {
			score[i][0] = -gap_penalty * i;
		}
		for (int i = 1; i < n; i++) {
			for (int j = 1; j < m; j++) {
				score[i][j] = max(score[i - 1][j] - gap_penalty,
						score[i][j - 1] - gap_penalty, score[i - 1][j - 1]
								+ s[getCode(a.charAt(i - 1))][getCode(b.charAt(j - 1))]);
			}
		}
		out.println(score[n - 1][m - 1]);
	}
}