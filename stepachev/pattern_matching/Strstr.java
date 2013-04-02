/**
 * Created with IntelliJ IDEA.
 * User: ingvard
 * Date: 22.03.13
 * Time: 13:56
 * To change this template use File | Settings | File Templates.
 */
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
    public static long hash(String s,int p,int mod)
    {
        int z=p;
        long h=0;

        for(int i=0; i < s.length();i++)
        {
            h+=(Integer.valueOf(s.charAt(i))*z)%mod;
            z=z*p;
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
    public static long pow(long a,long b)
    {
        long res=1;
        for(int i=0;i<b;i++)
            res=res*a;
        return res;
    }
    public static void rabKarp(String text,String pattern)
    {
        int p=5;
        int r=4294967;
        long hp=hash(pattern,p,r);
        long h=hash(text.substring(0,pattern.length()),p,r);
        for(int i=0;i<text.length()-pattern.length()+1;i++){
            if(h == hp)
                if(pattern.equals(text.substring(i,pattern.length()+i)))
                    System.out.print(i+" ");
            // h = (p * h - pow(p,pattern.length()) * hash(text.charAt(i),p,r) + hash(text.substring(i+pattern.length(),i+pattern.length()+1),p,r))%r;
            // System.out.println(i+" "+h+" "+hp);
            // System.out.println(text.substring(i,i+1)+" "+text.substring(i+pattern.length(),i+pattern.length()+1));

        }


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
    public static ArrayList<Integer> zFunction(String text,String pattern) //O(|T|+|P|)
    {
        ArrayList<Integer> result = new ArrayList<Integer>();
        int n=text.length()+pattern.length();
        int[] z = new int[n];
        String s=pattern+"#"+text;  //# - сентинел
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
                        i+=pattern.length()-1; //Буква не встретилась, сдвигаем на весь шаблон
                        break;
                    }
                    else
                    {
                        i+=pattern.length()-shift-2; //Сдвигаем на разность -2 так как номирация 2 раза с 0, а длины с 1.
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
       if(a.size() == b.size() && a.size() == b.size() && a.size() == c.size() &&
               a.size() == d.size() && a.size() == e.size() && a.size() == u.size())
               for(int i=0;i<a.size();i++)
                   if(a.get(i)!= b.get(i) || a.get(i) != b.get(i) || a.get(i) != c.get(i) ||
                           a.get(i) != d.get(i) || a.get(i) != e.get(i) || a.get(i) != u.get(i))
                                flag=1;
       return flag;
    }

    public static void test()
    {

    }

    public static void main(String[] arg) throws IOException
    {

         BufferedReader reader = new BufferedReader(new FileReader("/Users/ingvard/IdeaProjects/Strstr/src/DataSet.txt"));
         ArrayList<Integer> bf,pf,zf,rk,bc,gc;
         String text,pattern;
         while((text=reader.readLine()) != null){
            pattern=reader.readLine();
            bf=bruteForce(text,pattern);
            pf=pefixFunction(text,pattern);
            zf=zFunction(text,pattern);
            //rk=rabKarp("TGTGT","TGT");
            bc=badCharacterRule(text,pattern);
            System.out.println(correct(bc,pf,pf,pf,pf,pf));
         }
        rabKarp("TGTTGT","TGT");

    }



}
