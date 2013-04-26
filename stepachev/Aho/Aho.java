import com.sun.jmx.snmp.SnmpScopedPduRequest;

import java.util.LinkedList;
import java.util.Queue;

/**
 * Created with IntelliJ IDEA.
 * User: ingvard
 * Date: 18.04.13
 * Time: 13:52
 * To change this template use File | Settings | File Templates.
 */

class Node {
    public Node[] son;    // Список сыновей
    public Node go;
    public Node suffixLink;
    public Node parent;  // ссылка на родителя
    public boolean end;  // терменатор
    public int num; //Нумерация вершины
    public char charToParent; // Буква в вершине
    Node(int countSon)
    {
        son = new Node[countSon];
    }
}

class Tree {
    public int countNode;
    private Node root;
    private int powerAlp;

    Tree() {
        this.powerAlp = 80;
        this.countNode = 1;
        this.root = new Node(this.powerAlp);
        this.root.num = 0;
    }

    public Node searchLink(Node u,char a){

        int index = (int)(a - 'a');
        if( u == root)
            return root;
        if( u.suffixLink.son[index] != null)
        {
            return u.suffixLink.son[index];
        }
        else
        {
            return searchLink(u.parent,a);
        }

    }
    public void buildSuffixLink()
    {
        Queue<Node> nodeQueue = new LinkedList<Node>();
        // Создали ссылки на корень для 1 уровня вершин, и добавили их в очередь
        for(int i = 0; i < this.powerAlp ; i++)
        {
            if(root.son[i] != null)
            {
                root.son[i].suffixLink = root;
                nodeQueue.add(root.son[i]);
            }
        }
        //Производим обход в ширину
        while (nodeQueue.size() != 0)
        {
            Node qeNode = nodeQueue.remove();
            qeNode.suffixLink = searchLink(qeNode.parent,qeNode.charToParent);  // Рекурсивно вычисляем суффиксные ссылки
            for (int i = 0; i < qeNode.son.length; i++)
                if( qeNode.son[i] != null)
                    nodeQueue.add(qeNode.son[i]);
        }

    }
    public void addString(String str) {
        Node cur = root;
        for (int i = 0; i < str.length(); i++) {
            int index = (int) (str.charAt(i) - 'a');
            if (cur.son[index] == null) {
                cur.son[index] = new Node(this.powerAlp);
                cur.son[index].parent = cur;
                cur.son[index].end = false;
                cur.son[index].go = null;
                cur.son[index].suffixLink = null;
                cur.son[index].num = (countNode++);
                cur.son[index].charToParent = str.charAt(i);
            }
            cur = cur.son[index];
        }
        cur.end = true;
    }
}
public class Aho {
    public static void main(String[] arg) {
        Tree myTree = new Tree();

        myTree.addString("he");
        myTree.addString("she");
        myTree.addString("his");
        myTree.addString("hers");
        myTree.buildSuffixLink();
        System.out.println(myTree.countNode);
    }
}
