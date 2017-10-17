public class ParentsTree {

    class Node {
        public Node left;
        public Node right;
        public String name;

        Node(String name) {
            this.name = name;
        }

        public Node getLeft() {
          return left;
        }

        public Node getRight() {
          return right;
        }
    }

    private Node root;

    public ParentsTree(String name) {
      root = new Node(name);
    }

    public boolean search(String name) {
      return searchAux(root, name);
    }

    private boolean searchAux(Node node, String name) {
      if (node == null) {
        return false;
      }
      if (node.name == name) {
        return true;
      }
      return searchAux(node.left, name) || searchAux(node.right, name);
    }

    public int nElements() {
      return nElementsAux(root);
    }

    private int nElementsAux(Node node) {
      if (node == null) {
        return 0;
      } else {
        return 1 + nElementsAux(node.right) + nElementsAux(node.left);
      }
    }

    public int maxHeight() {
      return maxHeightAux(root);
    }

    private int maxHeightAux(Node node) {
      if (node == null) {
        return 0;
      } else {
        return Math.max(maxHeightAux(node.left)+1,maxHeightAux(node.right)+1);
      }
    }

    public String printTree() {
      return printTreeAux(root);
    }

    private String printTreeAux(Node node) {
      if (node == null) {
        return "";
      } else {
        return printTreeAux(node.left) + " "
          + node.name + " " + printTreeAux(node.right);
      }
    }

    public String getGrandMothersName(String grandChild) {
      return getGrandAux(root, grandChild);
    }

    public String getGrandAux(Node node, String name) {
      
    }

    public void testDavidParents() {
      root.left = new Node("Claudia");
      root.right = new Node("Gustavo");
      root.left.left = new Node("Ilva");
      root.left.right = new Node("Efrain");
      root.right.left = new Node("Astrid");
      root.right.right = new Node("Jose");
      root.right.left.left = new Node("Leonilde");
      root.right.left.right = new Node("Epaminondas");
    }

    public void testWilkensonParents() {
      root.left = new Node("Joaquina");
      root.right = new Node("Sufranio");
      root.left.left = new Node("Eustaquia");
      root.left.left.left = new Node("Florinda");
      root.left.right = new Node("Eustaquio");
      root.left.right.right = new Node("Jovin");
      root.right.left = new Node("Piolina");
      root.right.left.left = new Node("Wilberta");
      root.right.right = new Node("Piolin");
      root.right.right.right = new Node("Usnavy");
    }

    public static void main(String[] args) {

      ParentsTree bt = new ParentsTree("David");
      bt.testDavidParents();
      System.out.println("Search for 'Ilva' = " + bt.search("Ilva"));
      System.out.println("Search for 'Mariana' = " + bt.search("Mariana"));
      System.out.println("MaxHeight = " + bt.maxHeight());
      System.out.println("Number of elements = " + bt.nElements());
      System.out.println(bt.printTree());

      ParentsTree bt2 = new ParentsTree("Wilkenson");
      bt2.testWilkensonParents();
      System.out.println("Search for 'Jovin' = " + bt1.search("Jovin"));
      System.out.println("Search for 'Mariana' = " + bt1.search("Mariana"));
      System.out.println("MaxHeight = " + bt1.maxHeight());
      System.out.println("Number of elements = " + bt1.nElements());
      System.out.println(bt1.printTree());
    }

   /* testDavidParents
    *                           David
    *                          /      \
    *                         /        \
    *                        /          \
    *                       /            \
    *                Claudia              Gustavo
    *              /        \              /     \
    *            /           \            /       \
    *          Ilva       Efrain    Astrid         Jose
    *                              /     \
    *                       Leonilde     Epaminondas
    */
}
