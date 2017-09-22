from DataStructures import LinkedList, ArrayList, Queue, Stack
from Classes import Fridge, Order


def list_product(*nums):
    s = 1
    for i in nums:
        s *= i
    return s


def smart_insert(data, nums):
    try:
        nums.index(data)
    except ValueError:
        nums.append(data)

    return nums


def balance(to_balance):
    pass


def manage_fridges(fridges1, orders1):
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
    fridges = [Fridge(1, "haceb"), Fridge(2, "lg"), Fridge(3, "ibm"),
               Fridge(4, "haceb"), Fridge(5, "lg"), Fridge(6, "ibm"),
               Fridge(7, "haceb"), Fridge(8, "lg"), Fridge(9, "ibm"),
               Fridge(8, "lg"), Fridge(9, "ibm")]

    orders = [Order("eafit", 10), Order("la14", 2),
              Order("olimpica", 4), Order("exito", 1)]

    manage_fridges(fridges, orders)


