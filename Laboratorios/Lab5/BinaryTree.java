public class BinaryTree {

    class Node {
        public Node left;
        public Node right;
        public int data;
        Node(int data) {
            this.data = data;
        }
    }

    private Node root;

    public BinaryTree() {
        root = null;
    }

    /**
     * @param data the integers you want to insert to the binary tree
     */
    public void insert(int... data) {
        for(int obj: data)
            insert(obj);
    }

    /**
     * @param data the integer you want to insert to the binary tree
     */
    public void insert(int data) {
        if (root == null)
            root = new Node(data);
        else
            insert(root, data);
    }

    private void insert(Node n, int data) {
        if(n == null) {
            return;
        }
        if (n.data > data) {
            if (n.left == null)
                n.left = new Node(data);
            else
                insert(n.left, data);
        }
        else {
            if (n.right == null)
                n.right = new Node(data);
            else
                insert(n.right, data);
        }
    }

    /**
     * @return the string version of the tree
     */
    public String toString(){
        return auxPrint(root, 1);
    }
    private String auxPrint(Node n, int level) {
        if (n == null)
            return "";

        String result = "";
        result = "" + n.data + "\n";
        String tabs = "";
        for(int i = 0; i < level; i++) {
            tabs += "\t";
        }
        result += tabs + "|-------" + auxPrint(n.left, level + 1);
        result += "\n" + tabs + "|-------" + auxPrint(n.right, level+1);

        return result;

    }

    /**
     * @return the size of the tree
     */
    public int size(){
        return size(root);
    }
    private int size(Node n) {
        if (n == null)
            return 0;
        return 1 + size(n.left) + size(n.right);
    }

    /**
     * @return the depth of the binary tree
     */
    public int depth(){
        return depth(root);
    }
    private int depth(Node n) {
        if (n == null)
            return 0;
        return Math.max(depth(n.left), depth(n.right)) + 1;
    }

    /**
     * Prints the tree in pos-order
     */
    public void posOrder() {
        posOrder(root);
    }
    private void posOrder(Node n) {
        if (n == null)
            return;

        posOrder(n.left);
        posOrder(n.right);
        System.out.println("" + n.data);
    }

    /**
     * It clears the tree
     */
    public void clear(){
        root = null;
    }
}
