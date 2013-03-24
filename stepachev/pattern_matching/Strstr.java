/**
 * Created with IntelliJ IDEA.
 * User: ingvard
 * Date: 22.03.13
 * Time: 13:56
 * To change this template use File | Settings | File Templates.
 */
public class Strstr {
     public static void bruteForce(String text,String pattern)
     {
         for(int i=0;i<text.length()-pattern.length()+1;i++)  //O(|T|)
                 if(pattern.equals(text.substring(i,pattern.length()+i)))// O(|P|)
                     System.out.print(i+" ");
         System.out.println();
     }

     public static long hash(String s)
     {
         int p=5;
         int mod=100001;
         int z=p;
         long h=0;

         for(int i=0; i < s.length();i++)
         {
             h+=(Integer.valueOf(s.charAt(i))*z)%mod;
             z=z*p;
         }
         return h;
     }
     public static void rabKarp(String text,String pattern)
     {
         long hp=hash(pattern);
         long h=hash(text.substring(0,pattern.length()));
         int p=5;
         int r=100001;
         for(int i=0;i<text.length()-pattern.length();i++){

             if(hp == h)
             {
                System.out.print(i);
             }
             h = (p * h - p * hash(text.substring(i,i+1)) + hash(text.substring(i+pattern.length(),i+pattern.length()+1)))%r;
             if (h < 0)
                h += r;
             //System.out.println(h);
         }


     }
     public static void pefixFunction(String text,String pattern)
     {

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
                System.out.print((i-2*pattern.length()-1)+" ");
       }
       System.out.println();

    }
     public static void zFunction(String text,String pattern)
     {
         int n=text.length()+pattern.length();
         int[] z = new int[n];
         String s=pattern+"#"+text;
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
                System.out.print((i-pattern.length()-1)+" ");

     }

     public static void main(String[] arg)
     {
         System.out.println("bruteForce: ");
         bruteForce("AATGTGTCAA","TGT");
         System.out.println("pefixFunction: ");
         pefixFunction("AATGTGTCAA","TGT");
         System.out.println("zFunction: ");
         zFunction("AATGTGTCAA","TGT");
         System.out.println("rabKarp: ");
         rabKarp("AATGTGTCAA","TGT");
     }

}
