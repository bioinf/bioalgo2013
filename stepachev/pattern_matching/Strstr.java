/**
 * Created with IntelliJ IDEA.
 * User: ingvard
 * Date: 22.03.13
 * Time: 13:56
 * To change this template use File | Settings | File Templates.
 */
import com.sun.deploy.util.ArrayUtil;

import java.util.*;
import java.io.*;
public class Strstr {

    public static ArrayList<Integer> bruteForce(String text,String pattern)  //O(|T|*|P|)
    {
        ArrayList<Integer> result = new ArrayList<Integer>();
        for(int i=0;i<text.length()-pattern.length()+1;i++)  //O(|T|)
            if(pattern.equals(text.substring(i,pattern.length()+i)))// O(|P|)
                result.add(i);
        return result;
    }
    public static long hash(String s,int[] pow,int mod)
    {
        long h=0;
        /**
         * Example S[2]+S[1]P+S[0]P^2
         */
        for(int i=s.length()-1; i >= 0 ;i--)
        {
            h=(h+convert(s.charAt(s.length()-1-i))*pow[i])%mod;
        }
        return h;
    }
    public static int convert(char a)
    {
        switch (a){
            case 'A':
                return 1;
            case 'C':
                return 2;
            case 'G':
                return 3;
            case 'T':
                return 4;
            default:
                return 0;
        }
    }
    public static ArrayList<Integer> rabKarp(String text,String pattern)
    {
        int p=5;
        int r=45564345;
        ArrayList<Integer> result = new ArrayList<Integer>();
        int[] pow = new int[text.length()];
        pow[0]=1;
        for(int i=1;i<pow.length;i++)
            pow[i]+=(pow[i-1]*p);
        long h=hash(text.substring(0,pattern.length()),pow,r);
        long hp=hash(pattern,pow,r);
        for(int i=0;i<text.length()-pattern.length()+1;i++)
        {
            if(h == hp)
                if(pattern.equals(text.substring(i,pattern.length()+i)))
                    result.add(i);
            if(text.length()-pattern.length() > i)
                hp=(p*hp-pow[pattern.length()]*convert(text.charAt(i))+convert(text.charAt(i+pattern.length())))%r;
        }
        return result;
    }
    public static ArrayList<Integer> pefixFunction(String text,String pattern)
    {

        ArrayList<Integer> result = new ArrayList<Integer>();
        int[] p=new int[text.length()+pattern.length()+3];
        String s="$";
        s+=pattern+"#"+text;
        p[1]=0;
        int k=0;
        for(int i=2; i < s.length();i++)
        {
            while(k>0 && s.charAt(i) != s.charAt(k+1))
                k=p[k];
            if(s.charAt(i) == s.charAt(k+1))
                k++;
            p[i]=k;
        }
        for(int i=1; i < s.length();i++)
        {
            if(p[i] == pattern.length())
                result.add(i-2*pattern.length()-1);
        }
        return result;

    }
    public static int[] zFunction(String s) //O(|T|+|P|)
    {

        int n=s.length();
        int[] z=new int[n];
        int l=0;
        int r=0;
        for(int i=0; i < n;i++)
        {
            if(i > r) //Ищим Z функцию за приделами нашего отрезка
            {
                while (i+z[i] < n && s.charAt(z[i]) == s.charAt(z[i]+i))
                {
                    ++z[i];
                }
                if(z[i] > 0)
                {
                    r=i+z[i]-1;
                    l=i;
                }
            }
            else
            {
                z[i]=(r-l+1)>z[i-l]?z[i-l]:(r-l+1);
                while (i+z[i] < n && s.charAt(z[i]) == s.charAt(z[i]+i))
                {
                    ++z[i];
                }
                if(z[i] > 0)
                {
                    r=i+z[i]-1;
                    l=i;
                }
            }
        }
        return z;

    }
    public static ArrayList<Integer> kMPZ(String text,String pattern)
    {
        ArrayList<Integer> result =  new ArrayList<Integer>();
        int n=text.length()+pattern.length();
        String s=pattern+"#"+text;  //# - сентинел
        int[] z = zFunction(s);
        for(int i=0; i < n; i++)
            if(z[i] == pattern.length())
                result.add(i-pattern.length()-1);
        return result;
    }
    public static int nextRight(List<Integer>[] list,char x,int k)
    {
        //List список где хронятся вхождения букв в шаблон, x - символ который ищим, k - правее заданой позиции
        for(int i=0; i < list[convert(x)-1].size();i++)
            if(list[convert(x)-1].get(i) < k) return list[convert(x)-1].get(i);
        return -1;
    }
    public static ArrayList<Integer> badCharacterRule(String text,String pattern)
    {
        ArrayList<Integer> result = new ArrayList<Integer>();
        int shift;
        //Список для поиска правых вхождений
        List<Integer>[] arrChar = new List[4];
        for(int i=0;i<4;i++)
            arrChar[i]=new ArrayList<Integer>();
        //Препроцессинг
        for(int i=pattern.length()-1;i>=0;i--)
            arrChar[convert(pattern.charAt(i))-1].add(i);
        for(int i=0;i<text.length()-pattern.length()+1;i++)
        {
            for(int j=pattern.length()-1; j >=0;j--)
            {
                if(pattern.charAt(j) == text.charAt(i+j)){  //Полное вхождение
                    if(j == 0) result.add(i);
                }
                else
                {
                    shift=nextRight(arrChar,text.charAt(i+j),j); //Считаем нужный сдвиг
                    if(shift == -1)
                    {
                        i+=j-1;
                        break;
                    }
                    else
                    {
                        i+= j - shift-1;
                        break;
                    }
                }
            }
        }
        return result;
    }
    public static ArrayList<Integer> galilRule(String text,String pattern)
    {
        ArrayList<Integer> result = new ArrayList<Integer>();
        int shift,next;
        //Список для поиска правых вхождений
        List<Integer>[] arrChar = new List[4];
        for(int i = 0 ; i < 4 ; i++ )
            arrChar[i] = new ArrayList<Integer>();
        //Препроцессинг
        for(int i = pattern.length() - 1 ; i >= 0 ; i-- )
            arrChar[ convert( pattern.charAt(i) ) - 1 ].add(i);
        int[] z=zFunction(new StringBuffer(pattern).reverse().toString());
        int [] L = new int[ pattern.length() ];
        for (int j = 0; j < pattern.length(); j++ ) {
            if(z[pattern.length() - j - 1] != 0)
            {
                int i = pattern.length() - z[pattern.length() - j - 1];
                L[i] = j;
            }
        }
        for(int i=0;i<text.length()-pattern.length()+1;i++)
        {
            int right=-1;
            for(int j=pattern.length()-1; j >=0;j--)
            {
                if( j == right)
                {
                    j-=z[pattern.length() - j - 1];
                    right=-1;
                }
                else{
                    if(pattern.charAt(j) == text.charAt(i+j)){  //Полное вхождение
                        if(j == 0) result.add(i);
                    }
                    else
                    {
                        shift=( pattern.length() - 1 ) != j ? pattern.length() - 2 - L[j+1] : 0;
                        right=shift+pattern.length()+1;
                        i+=shift;
                        break;
                    }
                }
            }
        }

      return result;
    }
    public static int correct (ArrayList<Integer> a,ArrayList<Integer> b, ArrayList<Integer> c,
                          ArrayList<Integer> d, ArrayList<Integer> e,ArrayList<Integer> u )
    {
        int flag=0;
        if(a.size() != b.size() && a.size() != b.size() && a.size() != c.size() &&
                a.size() != d.size() && a.size() != e.size() && a.size() != u.size())
            for(int i=0;i<a.size();i++)
                if(a.get(i)!= b.get(i) || a.get(i) != b.get(i) || a.get(i) != c.get(i) ||
                        a.get(i) != d.get(i) || a.get(i) != e.get(i) || a.get(i) != u.get(i))
                    flag=1;
        return flag;
    }


    public static void main(String[] arg) throws IOException
    {

        BufferedReader reader = new BufferedReader(new FileReader("C:\\Users\\ingvard\\IdeaProjects\\Strstr\\src\\DataSet.txt"));
        BufferedWriter output = new BufferedWriter(new FileWriter("C:\\Users\\ingvard\\IdeaProjects\\Strstr\\src\\report.txt"));
        ArrayList<Integer> bf,pf,zf,rk,bc,gc;
        String text,pattern;
        long[] result = new long[6];
        long time;
        while((text=reader.readLine()) != null){
            pattern=reader.readLine();
            Arrays.fill(result,0);
            output.write("Test string: "+text+" \n pattern: "+pattern+" \n");
            for(int i=0;i<1000;i++)
            {
                time = System.currentTimeMillis();
                bf=bruteForce(text, pattern);
                result[0]+=(System.currentTimeMillis()-time);
                time = System.currentTimeMillis();
                pf=pefixFunction(text,pattern);
                result[1]+=(System.currentTimeMillis()-time);
                time = System.currentTimeMillis();
                zf=kMPZ(text,pattern);
                result[2]+=(System.currentTimeMillis()-time);
                time = System.currentTimeMillis();
                rk=rabKarp(text,pattern);
                result[3]+=(System.currentTimeMillis()-time);
                time = System.currentTimeMillis();
                bc=badCharacterRule(text,pattern);
                result[4]+=(System.currentTimeMillis()-time);
                time = System.currentTimeMillis();
                gc=galilRule(text,pattern);
                result[5]+=(System.currentTimeMillis()-time);
            }
            output.write("bruteForce: " + (result[0]) + " ms \n");
            output.write("pefixFunction: "+(result[1])+" ms \n");
            output.write("kMPZ: "+(result[2])+" ms \n");
            output.write("rabKarp: "+(result[3])+" ms \n");
            output.write("badCharacterRule: "+(result[4])+" ms \n");
            output.write("galilRule: "+(result[5])+" ms \n");
            output.write("The total length: text "+text.length()*1000+" patter "+pattern.length()*1000+" \n ********************************************************************** \n");


        }
        output.close();
    }
}
