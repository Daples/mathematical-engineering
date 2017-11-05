
class DigraphAM:
    class GraphObj:
        def __init__(self, value, weight, dict):
            self.value = value
            self.weight = weight
            self.dict = dict

        def __str__(self):
            return "Value:" + self.value + ", " + "Weight:" + self.weight \
                   + ", Extra arguments:" + self.dict

    def __init__(self, n):
        self.matrix = [[None] * n for e in range(n)]
        self.n = n

    def insert(self, parent, child, weight=0, **kwargs):
        if parent in range(self.n) and child in range(self.n):
            self.matrix[parent][child] = DigraphAM.GraphObj(1, weight, kwargs)
        else:
            print("The digraph only receives numbers between 0 and", self.n - 1)

    def search(self, parent):
        child = []
        if parent in range(self.n):
            for i in range(len(self.matrix[parent])):
                if self.matrix[parent][i] is not None:
                    child.append(i)
        else:
            print("The digraph only receives numbers between 0 and", self.n - 1)
        return child

    def are_related(self, parent, child):
        return parent in range(self.n) and child in range(self.n) \
               and self.matrix[parent][child] is not None

    def __str__(self):
        return str(self.matrix)

    def weight(self, parent, child):
        if parent in range(self.n) and child in range(self.n):
            if self.matrix[parent][child] is not None:
                return self.matrix[parent][child].weight
        return -1


class DigraphAL:
    def __init__(self, n):
        self.ar = [Ll() for e in range(n)]
        self.n = n

    def insert(self, parent, child, weight=0, **kwargs):
        if parent in range(self.n) and child in range(self.n):
            self.ar[parent].insert(DigraphAM.GraphObj(child, weight, kwargs))
        else:
            print("The digraph only receives numbers between 0 and", self.n - 1)

    def search(self, parent):
        if parent in range(self.n):
            children = []
            for link in self.ar[parent]:
                children.append(link.value)
            return children
        else:
            print("The digraph only receives numbers between 0 and", self.n - 1)

    def are_related(self, parent, child):
        if parent in range(self.n):
            for link in self.ar[parent]:
                if link.value == child:
                    return True

        return False

    def __str__(self):
        string = "["
        for item in self.ar:
            string += str(item)
            if item is not self.ar[-1]:
                string += ", "

        return string + "]"

    def weight(self, parent, child):
        if parent in range(self.n):
            for link in self.ar[parent]:
                if link.value == child:
                    return link.weight
        return -1

class LinkedList(object):

    class Node(object):
        def __init__(self, node):
            self.node = node
            self.next = None
            self.prev = None

        def __str__(self):
            return str(self.node)

    def __init__(self):
        self.first = None
        self.int_size = 0
        self.last = None

    def __len__(self):
        """
        :return: the size of the linked list
        """
        return self.int_size

    def insert_multi(self, *objs):
        """
        :param objs: objects to insert in the linked list
        :return: nothing
        """
        for obj in objs:
            self.insert(obj, self.int_size)

    def insert(self, obj, i=0):
        """
        :param obj: the object you want to insert
        :param i: the index you want to insert the object
        :return: nothing
        """
        if i > self.int_size:
            print("Index out of bounds")
            return None
        else:
            obj_node = LinkedList.Node(obj)
            mov_obj = self.first
            if mov_obj is None:
                self.first = obj_node
                self.last = obj_node
                self.int_size += 1
                return None
            elif i == 0:
                self.first.prev = obj_node
                obj_node.next = self.first
                self.first = obj_node
                self.int_size += 1
                return None
            elif i == self.int_size:
                obj_node.prev = self.last
                self.last.next = obj_node
                self.last = obj_node
                self.int_size += 1
                return None
            elif i < self.int_size / 2:
                for j in range(i):
                    if j <= i - 1:
                        last = mov_obj
                    mov_obj = mov_obj.next

                obj_node.next = mov_obj
                obj_node.prev = mov_obj.prev
                mov_obj.prev = obj_node
                last.next = obj_node
            else:
                j = self.int_size - 1
                mov_obj = self.last
                while j >= i:
                    if j == i:
                        last = mov_obj
                    mov_obj = mov_obj.prev
                    j -= 1

                obj_node.next = mov_obj.next
                obj_node.prev = mov_obj
                mov_obj.next = obj_node
                last.prev = obj_node

            self.int_size += 1
            return obj

    def get(self, i):
        """
        :param i: the index you want to get the object
        :return: the object at index i
        """
        if i >= self.int_size:
            print("The index passed doesn't exist on the list")
            return None
        else:
            if i > self.int_size/2:
                j = self.int_size - 1
                temp_node = self.last
                while j > i:
                    temp_node = temp_node.prev
                    j -= 1
            else:
                temp_node = self.first
                for j in range(i):
                    temp_node = temp_node.next

            return temp_node.node

    def remove(self, i):
        """
        :param i: the index of the object you want to remove
        :return: the object removed
        """
        if i >= self.int_size:
            print("Index out of bounds")
            return None
        else:
            if self.int_size == 1:
                self.first = None
                self.last = None
                self.int_size -= 1
                return
            elif i == 0:
                erased = self.first
                self.first.next.prev = None
                self.first = self.first.next
                self.int_size -= 1
                return erased.node
            elif i == self.int_size - 1:
                erased = self.last
                self.last.prev.next = None
                self.last = self.last.prev
                self.int_size -= 1
                return erased.node
            elif i > self.int_size/2:
                temp_node = self.last
                j = self.int_size - 1
                while j > i:
                    temp_node = temp_node.prev
                    j -= 1
            else:
                temp_node = self.first
                for j in range(i):
                    temp_node = temp_node.next
            erased = temp_node
            temp_node.prev.next = temp_node.next
            temp_node.next.prev = temp_node.prev
            return erased.node

    def clear(self):
        """
        :return: nothing
        """
        self.first = None
        self.last = None
        self.int_size = 0

    def __str__(self):
        """
        :return: a string version of the linked list
        """
        temp_obj = self.first
        acum = ""
        while temp_obj is not None:
            if temp_obj is not self.last:
                acum += str(temp_obj.node) + " <-> "
            else:
                acum += str(temp_obj.node)
            temp_obj = temp_obj.next
        return acum

    def __contains__(self, item):
        """
        :param item: the item you want to search for
        :return: if the item is in the list
        """
        for i in self:
            if i is item:
                return True
        return False

    def to_list(self):
        """
        :return: a iterable version of the linked list
        """
        temp_object = self.first
        while temp_object is not None:
            yield temp_object.node
            temp_object = temp_object.next

    def __iter__(self):
        """
        :return: a iterable object of the list
        """
        return self.to_list()

    def size(self):
        """
        :return: the size of the list
        """
        return self.int_size

    def get_first(self):
        """
        :return: the value of the first node
        """
        return self.first.node

    def get_last(self):
        """
        :return: the value of the last node
        """
        return self.last.node


class Queue:

    def __init__(self):
        self.ll = LinkedList()

    def push(self, obj):
        """
        :param obj: the object you want to insert
        :return: nothing
        """
        self.ll.insert(obj, 0)

    def push_multi(self, *objs):
        """
        :param objs: the objects to insert in the queue in the order they arrived
        :return: nothing
        """
        for obj in objs:
            self.push(obj)

    def peek(self):
        """
        :return: the item that first inserted it the queue
        """
        return self.ll.get_last()

    def pop(self):
        """
        :return: the element that first was inserted in the queue
        """
        temp_obj = self.ll.last
        self.ll.remove(self.ll.size() - 1)
        return temp_obj

    def size(self):
        """
        :return: the size of the queue
        """
        return self.ll.size()

    def __str__(self):
        """
        :return: a string version of the queue
        """
        return str(self.ll)


class Stack:

    def __init__(self, size):
        """
        :param size: maximum size of the stack
        """
        self.max_size = size
        self.ll = LinkedList()

    def push_multi(self, *objs):
        """
        :param objs: the objects you want to insert
        :return: nothing
        """
        for obj in objs:
            self.ll.insert(obj, self.ll.size())

    def push(self, obj):
        """
        :param obj: the object you want to insert
        :return: nothing
        """
        if self.ll.size() < self.max_size:
            self.ll.insert(obj, self.ll.size())
        else:
            print("Stack overflow")

    def peek(self):
        """
        :return: the object that last entered the stack
        """
        return self.ll.get_last()

    def pop(self):
        """
        :return: the first element in the stack
        """
        temp_object = self.ll.get_last()
        self.ll.remove(self.ll.size() - 1)
        return temp_object

    def size(self):
        """
        :return: the size of the stack
        """
        return self.ll.size()

    def __str__(self):
        """
        :return: a string version of the stack
        """
        acum = " "
        for item in self.ll:
            acum += str(item) + " "
        return acum

    def clear(self):
        """
        :return: nothing
        """
        self.ll.clear()
