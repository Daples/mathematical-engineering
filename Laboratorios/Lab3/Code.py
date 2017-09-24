from DataStructures import LinkedList, ArrayList, Stack
from Classes import Fridge, Order


def list_product(nums):
    """
    :param nums: list with numbers
    :return: the multiplication of the items
    """
    s = 1
    for i in nums:
        s *= i
    return s


def smart_insert(data, nums):
    """
    :param data: a value to insert
    :param nums: a list with objects
    :return: the array with the data inserted, if it doesn't already exists
    """
    for item in nums:
        if data == item:
            return

    nums.insert(data, nums.size())
    return nums


def balance(to_balance):
    """
    :param to_balance: a list with numbers
    :return: the index to balance the list
    """
    if to_balance.size() <= 1:
        print("There's nothing to balance")
        return
    total = 0
    array = []
    for item in to_balance:
        total += item

    for i in range(1, len(to_balance)):
        sum = 0
        for j in range(i):
            sum += to_balance.get(j)
        array.append(sum)

    min = total - 2*array[0] - to_balance.get(1)
    for i in range(len(array)):
        if abs(min) >= abs(total - 2*array[i] - to_balance.get(i + 1)):
            min = total - 2*array[i] - to_balance.get(i + 1)
            min_index = i + 1

    return min_index


def manage_fridges(fridges1, orders1):
    """
    This is using linked list implicitly
    :param fridges1: a list with fridges
    :param orders1: a list with orders
    :return: nothing, it prints the orders and the fridges assigned
    """
    # Putting the fridges and orders in the right data structure
    fridges = Stack(len(fridges1))
    for fridge in fridges1:
        fridges.push(fridge)
    orders = Stack(len(orders1))
    for order in orders1:
        orders.push(order)

    # Code for distributing the fridges
    while fridges.size() != 0 or orders.size() != 0:
        attending = orders.pop()
        acum = "(" + str(attending) + ", ["
        while attending.num > 0:
            if attending.num > 1:
                acum += str(fridges.pop()) + " "
            else:
                acum += str(fridges.pop())
            attending.num -= 1
            if fridges.size() == 0:
                break
        acum += "])"
        print(acum)


def exercise_4():
    """
    :return: nothing, it resolves the exercise 4
    """
    fridges = [Fridge(1, "haceb"), Fridge(2, "lg"), Fridge(3, "ibm"),
               Fridge(4, "haceb"), Fridge(5, "lg"), Fridge(6, "ibm"),
               Fridge(7, "haceb"), Fridge(8, "lg"), Fridge(9, "ibm"),
               Fridge(8, "lg"), Fridge(9, "ibm")]

    orders = [Order("eafit", 10), Order("la14", 2),
              Order("olimpica", 4), Order("exito", 1)]

    manage_fridges(fridges, orders)


def manage_string(string):
    ll = LinkedList()
    array = string.split("\n")
    resp = ""
    for line in array:
        ll.clear()
        index = 0
        for char in line:
            if char == "[":
                index = 0
            elif char == "]":
                index = ll.size()
            else:
                ll.insert(char, index)
                index += 1

        for item in ll:
            resp += item
        resp += "\n"

    return resp


def exercise_2_1():
    resp = manage_string(input("Start typing (press enter to finish):\n"))
    print(resp)
    return resp

