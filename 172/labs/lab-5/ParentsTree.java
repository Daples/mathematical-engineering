public class ParentsTree {

    class Node {
        public Node left;
        public Node right;
        public String name;

        Node(String name) {
            this.name = name;
        }
    }

    private Node root;

    public ParentsTree(String name) {
      root = new Node(name);
    }

    /**
     * @param name name you want to search for.
     * @return whether the name is in the tree or not.
     */
    public boolean search(String name) {
      return searchAux(root, name);
    }

    private boolean searchAux(Node node, String name) {
      if (node == null) {
        return false;
      }
      if (node.name.equals(name)) {
        return true;
      }
      return searchAux(node.left, name) || searchAux(node.right, name);
    }
    /**
     * @return the number of elements in the tree.
     */
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
    /**
     * @return the max height or depth of the tree.
     */
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

    /**
     * @return string version of the tree.
     */
    public String toString() {
      return toStringAux(root);
    }

    private String toStringAux(Node node) {
      if (node == null) {
        return "";
      } else {
        return toStringAux(node.left) + " "
          + node.name + " " + toStringAux(node.right);
      }
    }

    private static Node searchNode(Node node, String name) {
      if (node != null) {
        if (node.name.equals(name)) {
          return node;
        } else {
          Node nodeAux = searchNode(node.left, name);
          if (nodeAux == null) {
            nodeAux = searchNode(node.right, name);
          }
          return nodeAux;
        }
      } else {
        return null;
      }
    }
    /**
     * @param grandChild name of the grandchild.
     * @return name of grandmother's name of the node passed.
     */
    public String getGrandMothersName(String grandChild) {
      return getGrandAux(root, grandChild);
    }

    public String getGrandAux(Node node, String name) {
      if (search(name)) {
        Node grandChild = searchNode(root, name);
        if (grandChild.left != null) {
          if (grandChild.left.left != null) {
            return grandChild.left.left.name;
          } else {
            return "GrandMa doesn't exist.";
          }
        } else {
          return "Doesn't have.";
        }
      } else {
        return "GrandChild doesn't exist.";
      }
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
      System.out.println(" - My example - ");
      ParentsTree bt = new ParentsTree("David");
      bt.testDavidParents();
      System.out.println("Search for 'Ilva' = " + bt.search("Ilva"));
      System.out.println("Search for 'Mariana' = " + bt.search("Mariana"));
      System.out.println("MaxHeight = " + bt.maxHeight());
      System.out.println("Number of elements = " + bt.nElements());
      System.out.println(bt.toString());
      System.out.println("David's grandma = " + bt.getGrandMothersName("David"));
      System.out.println("Gustavo's grandma = " + bt.getGrandMothersName("Gustavo"));
      System.out.println("Leonilde's grandma = " + bt.getGrandMothersName("Leonilde"));
      System.out.println("Mariana's grandma = " + bt.getGrandMothersName("Mariana"));

      System.out.println("\n - Wilkenson's example - ");
      ParentsTree bt1 = new ParentsTree("Wilkenson");
      bt1.testWilkensonParents();
      System.out.println("Search for 'Jovin' = " + bt1.search("Jovin"));
      System.out.println("Search for 'Mariana' = " + bt1.search("Mariana"));
      System.out.println("MaxHeight = " + bt1.maxHeight());
      System.out.println("Number of elements = " + bt1.nElements());
      System.out.println(bt1.toString());
      System.out.println("Wilkenson's grandma = " + bt1.getGrandMothersName("Wilkenson"));
      System.out.println("Sufranio's grandma = " + bt1.getGrandMothersName("Sufranio"));
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
