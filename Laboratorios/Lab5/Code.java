import java.util.Scanner;

public class Code {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in); //c1
        System.out.println("Write quit to end the program"); //c2
        String input = sc.next(); //c3
        BinaryTree bt = new BinaryTree(); //c4
        while(!input.equals("quit")) { // c5*n
            int node = Integer.parseInt(input); // c6*n
            bt.insert(node); // c7*n*logn
            input = sc.next(); //c8*n
        }

        bt.posOrder(); // O(n)
    }
}
