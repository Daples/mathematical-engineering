from DataStructures import LinkedList, Stack

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    WARNING = '\033[93m'
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    UNDERLINE = '\033[4m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'


def tests():
    ll = LinkedList()
    test = ll.remove(0)
    if test is None:
        print(bcolors.OKGREEN + "Removed succesfuly with empty list!" + bcolors.ENDC)

    ll.insert(5, 0)
    if ll.get_last() == 5:
        print(bcolors.OKGREEN + "Inserted successfully at first with empty list!" + bcolors.ENDC)

    ll.clear()
    ll.insert(5, ll.size())
    if ll.get_first() == 5:
        print(bcolors.OKGREEN + "Inserted successfully at last with empty list!" + bcolors.ENDC)

    ll.clear()
    test = ll.insert(5, ll.size() + 10)
    if test is None:
        print(bcolors.OKGREEN + "Inserted successfully with empty list!" + bcolors.ENDC)

    ll.clear()
    ll.insert_multi(1,2,3,4)
    ll.insert(5,0)
    if ll.get_first() == 5:
        print(bcolors.OKGREEN + "Inserted successfully at first!" + bcolors.ENDC)

    ll.remove(0)
    if ll.get_first() == 1:
        print(bcolors.OKGREEN + "Removed succesfully the first!" + bcolors.ENDC)


    ll.insert(5, ll.size())
    if ll.get_last() == 5:
        print(bcolors.OKGREEN + "Inserted successfully at last!" + bcolors.ENDC)

    ll.remove(ll.size() - 1)
    if ll.get_last() == 4:
        print(bcolors.OKGREEN + "Removed succesfully at last!" + bcolors.ENDC)


def robotic_arm():
    def pile_stacks(stack1, stack2):
        temp_stack = Stack(stack2.size())
        while stack2.size() != 0:
            temp_stack.push(stack2.pop())

        while temp_stack.size() != 0:
            stack1.push(temp_stack.pop())

    def sum_stacks(stack1, stack2):
        while stack2.size() != 0:
            stack1.push(stack2.pop())

    def operation(command):
        array = command.split(" ")
        found_a = False
        op1 = ""
        op2 = ""
        a = -1
        b = -1
        for item in array:
            if item == "move" or item == "pile":
                op1 = item
            elif item.isdigit():
                if not found_a:
                    a = int(item)
                    found_a = True
                else:
                    b = int(item)
            elif item == "onto" or item == "over":
                op2 = item

        return op1, a, op2, b

    def move_over(linked, a, b, n):
        stack = Stack(n)
        for item in linked:
            while item.size() != 0:
                stack.push(item.pop())
                if stack.peek() == a:
                    stack.pop()
                    while stack.size() != 0:
                        x = stack.pop()
                        linked.get(x).push(x)

            sum_stacks(item, stack)

        stack.clear()
        end = False
        for item in linked:
            while item.size() != 0:
                stack.push(item.pop())
                if stack.peek() == b:
                    end = True
                    break
            sum_stacks(item, stack)
            if end:
                item.push(a)
                break

    def move_onto(linked, a, b, n):
        move_over(linked, a, b, n)
        stack = Stack(n)
        for item in linked:
            while item.size() != 0:
                stack.push(item.pop())
                if stack.peek() == a:
                    while True:
                        x = item.pop()
                        if x == b:
                            stack.push(x)
                            break
                        linked.get(x).push(x)
            sum_stacks(item, stack)

    def pile_over(linked, a, b, n):
        stack = Stack(n)
        end_search = False
        a_pile = Stack(n)
        for item in linked:
            while item.size() != 0:
                stack.push(item.pop())
                if stack.peek() == a:
                    end_search = True
                    break
            if end_search:
                pile_stacks(a_pile, stack)
                break
            else:
                sum_stacks(item, stack)

        end = False
        for item in linked:
            while item.size() != 0:
                stack.push(item.pop())
                if stack.peek() == b:
                    end = True
                    break
            sum_stacks(item, stack)
            if end:
                sum_stacks(item, a_pile)
                break

    def pile_onto(linked, a, b, n):
        pile_over(linked, a, b, n)
        stack = Stack()
        for item in linked:
            while item.size() != 0:
                stack.push(item.pop())
                if stack.peek() == b:
                    item.push(stack.pop())
                    while stack.size() != 0:
                        x = stack.pop()
                        if x == a:
                            break
                        linked.get(x).push(x)
            sum_stacks(item, stack)

    def same_column(linked):
        stack = Stack(n)
        for link in ll:
            found_a = False
            found_b = False
            while link.size() != 0:
                stack.push(link.pop())
                if stack.peek() == a:
                    found_a = True
                elif stack.peek() == b:
                    found_b = True
            sum_stacks(link, stack)
            if found_a and found_b:
                return True
            elif found_a or found_b:
                return False
        return False

    n = int(input("Put the number of blocks you want to have: \n"))
    ll = LinkedList()
    for i in range(n):
        stack = Stack(n)
        stack.push(i)
        ll.insert(stack, ll.size())

    while True:
        command = input("").lower()
        if command == "quit":
            break
        op1, a, op2, b = operation(command)

        if a == b:
            if a == -1:
                print("Insert a valid operation")
                continue
            print("Error: Inserted the same numbers")
            continue

        if same_column(ll):
            print("They're in the same column")
            continue

        if a < 0 or b < 0 or a >= n or b >= n:
            print("Error: The numbers are not valid")
            continue

        if op1 == "move":
            if op2 == "over":
                move_over(ll, a, b, n)
            elif op2 == "onto":
                move_onto(ll, a, b, n)
        elif op1 == "pile":
            if op2 == "over":
                pile_over(ll, a, b, n)
            elif op2 == "onto":
                pile_onto(ll, a, b, n)

    i = 0
    for item in ll:
        string = str(i) + ":" + str(item)
        print(string)
        i += 1

robotic_arm()