public class BinarySearch {
  Node root;

  public BinarySearch (Node node) {
    root = node;
  }

  public void addNode (Node start, Node toAdd) {
    if (start == null) {
      System.out.println("Nope.");
      return;
    }
    if (start.value <= toAdd.value) {
      if (start.left == null) {
        start.left = toAdd;
        return;
      } else {
        addNode(start.left,toAdd);
      }
    } else {
      if (start.right == null) {
        start.right = toAdd;
        return;
      } else {
        addNode(start.right,toAdd);
      }
    }
  }

  public void printTree(Node node) {
    if (node != null) {
      System.out.println(node.value);
      printTree(node.left);
      printTree(node.right);
    }

  }

  public int nElements(Node node) {
    if (node == null) {
      return 0;
    } else {
      return 1 + nElements(node.left) + nElements(node.right);
    }
  }

  public int maxDepth(Node node) {
    if (node == null) {
      return 0;
    } else {
      return Math.max(maxDepth(node.right),maxDepth(node.left)) + 1;
    }
  }

  public static void printBinaryTree(Node root, int level) { // TEST
    if (root == null)
         return;
    printBinaryTree(root.right, level+1);
    if (level != 0){
        for(int i=0;i<level-1;i++)
            System.out.print("|\t");
            System.out.println("|-------" + root.value);
    } else {
        System.out.println(root.value);
    }
    printBinaryTree(root.left,level + 1);

  }

  public static void main(String[] args) {
    BinarySearch b1 = new BinarySearch(new Node(1));
    Node n1 = new Node(2);
    b1.addNode(b1.root,n1);
    Node n2 = new Node(-1);
    b1.addNode(b1.root,n2);
    Node n3 = new Node(3);
    b1.addNode(b1.root,n3);
    Node n4 = new Node(2);
    b1.addNode(b1.root,n4);
    Node n5 = new Node(-0.5);
    b1.addNode(b1.root,n5);
    Node n6 = new Node(4);
    b1.addNode(b1.root,n6);
    Node n7 = new Node(5);
    b1.addNode(b1.root,n7);

    System.out.println("N of Elements = " + b1.nElements(b1.root));
    System.out.println("Max Depth = " + b1.maxDepth(b1.root));
    printBinaryTree(b1.root,0);
  }
}
