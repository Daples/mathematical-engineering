public class Node {
  double value;
  Node left;
  Node right;
  Node parent;

  public Node (double value) {
    this.value = value;
    left = null;
    right = null;
    parent = null;
  }

  public void setLeft (Node node) {
    left = node;
  }

  public void setRight (Node node) {
    right = node;
  }

  
}
