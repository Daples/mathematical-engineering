public class MyLinkedList<E> {
    
    private Node<E> first;
    public static class Node<E>{
        public E node;
        public Node<E> next;

        public Node(E node, Node<E> next) {
            this.node = node;
            this.next = next;
        }    
        public Node(E node){
            this.node = node;
            next = null;
        }
    }
    
    
    
    private int size;
    
    public MyLinkedList(){
    	size = 0;
        first = null;
    }
    
    
    public static int maximum(MyLinkedList<Integer> myList){
    	if (myList.size() != 0) return maxAux(myList.first);
    	else throw new NullPointerException();
    }
    private static int maxAux(Node<Integer> p) {
    	if (p.next == null) return p.node;
    	
    	int max = maxAux(p.next);
    	if (max > p.node)
    		return max;
    	return p.node;
    }
    
    public static boolean compareTo(MyLinkedList<Integer> list1, MyLinkedList<Integer> list2){
    	if (list1.size() != list2.size()) return false;
    	else if(list1.size() == 0 && list2.size()==0) return true;
    	else {
    		boolean hasEqual = false;
    		Node<Integer> l1 = list1.first;
    		Node<Integer> l2;
    		for (int i = 0; i < list1.size(); i++){
    			l2 = list2.first;
    			for (int j = 0; j < list2.size(); j++){
    				if (l2.node == l1.node){
    					hasEqual = true;
    					break;
    				}
    				l2 = l2.next;
    			}
    			if (!hasEqual) return false;
    			hasEqual = false;
    		}
    		return true;
    	}
    }
    public void insert(E toAdd, int i){
        if (size < i) throw new IndexOutOfBoundsException();
        else if (toAdd == null) throw new NullPointerException();
        else if (i == 0) insertFirst(toAdd);
        else {
            Node<E> temp = first;
            for (int j = 0; j < i-1; j++)
                temp = temp.next;

            Node aft = temp.next;
            Node<E> adder = new Node<>(toAdd);
            adder.next = aft;
            temp.next = adder;
        }
        size++;
    }
    public void insertFirst(E toAdd){
        if (first != null) {
            Node<E> adder = new Node<>(toAdd);
            adder.next = first;
            first = adder;
            size++;
        } else {
            first = new Node<>(toAdd);
        }
    }

    public void insert(E... toAdd){
        for (E temp: toAdd)
            insert(temp,size);
    }
    
    public void delFinal(){
        if(size >= 2) {
            Node<E> temp = first;
            while(temp.next.next != null)
                temp = temp.next;
            temp.next = null;
        } else if (size == 1){
            first = null;
        }
        if (size != 0) size--;
    }
    public void delFirst(){
        if (size >= 2)
            first = first.next;
        else
            first = null;
        size--;
    }
    public void backPrint(){
        Node<E> temp;
        for (int i = 0; i < size; i++){
            temp = first;
            for(int j = 0; j < size-i-1; j++) 
                temp = temp.next; 
            System.out.println(temp.node);
        }
    }
    public void print(){
        Node<E> temp = first;
        for(int i = 0; i < size; i++){
            System.out.println(temp.node);
            temp = temp.next;
        }
    }
    public int size(){
    	return size;
    }
    
    public static void main(String[] args){
        MyLinkedList<Integer> myList = new MyLinkedList<>();
        myList.insert(8,9,10,33,22,44,90,70,50);
        MyLinkedList<Integer> myList2 = new MyLinkedList<>();
        myList2.insert(50,70,90,44,22,33,10,9);
        System.out.println(MyLinkedList.compareTo(myList,myList2));
    }
}
