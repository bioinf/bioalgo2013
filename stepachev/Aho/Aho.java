import java.util.ArrayList;

/**
 * Created with IntelliJ IDEA.
 * User: ingvard
 * Date: 18.04.13
 * Time: 13:52
 * To change this template use File | Settings | File Templates.
 */

class Vertex {
    public char letter;
    public Tria link;

    Vertex(char a, Tria b) {
        letter = a;
        link = b;
    }
}

//Вершина бора.
class Tria {
    public int num;  // Номер указывает на конец i слова в этой вершине.
    public ArrayList<Vertex> arrChar = new ArrayList<Vertex>();

    Tria(int n) {
        num = n;
    }
}

public class Aho {

    public static Tria root = new Tria(0);
    public static int countPattern = 0;

    public static void add(String text, Tria roots) {
        int flag = 0;
        //Перебераем все исходящие из вершины рёбра.
        for (int i = 0; i < roots.arrChar.size(); i++) {
            if (roots.arrChar.get(i).letter == text.charAt(0)) {
                add(text.substring(1, text.length()), roots.arrChar.get(i).link);
                flag = 1;
                break;
            }
        }
        //Добавляем новое ребро
        if (flag == 0 && text.length() != 0) {
            if (text.length() == 1) {
                countPattern++;
                roots.arrChar.add(new Vertex(text.charAt(0), new Tria(countPattern)));
            } else {
                roots.arrChar.add(new Vertex(text.charAt(0), new Tria(0)));
                add(text.substring(1, text.length()), roots.arrChar.get(roots.arrChar.size() - 1).link);
            }
        }
    }

    public static void main(String[] arg) {
        add("he", root);
        add("she", root);
        add("his", root);
        add("hers", root);
        System.out.println(countPattern);
    }
}
