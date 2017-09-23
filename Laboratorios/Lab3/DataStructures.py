class LinkedList:

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

    def insert_multi(self, *objs):
        for obj in objs:
            self.insert(obj, self.int_size)

    def insert(self, obj, i=0):
        if i > self.int_size:
            print("Index out of bounds")
            return
        else:
            obj_node = LinkedList.Node(obj)
            mov_obj = self.first
            if mov_obj is None:
                self.first = obj_node
                self.last = obj_node
                self.int_size += 1
                return
            elif i == 0:
                self.first.prev = obj_node
                obj_node.next = self.first
                self.first = obj_node
                self.int_size += 1
                return
            elif i == self.int_size:
                obj_node.prev = self.last
                self.last.next = obj_node
                self.last = obj_node
                self.int_size += 1
                return
            elif i < self.int_size / 2:
                for j in range(i):
                    if j == i - 1:
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

    def get(self, i):
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

            return temp_node

    def remove(self, i):
        if i >= self.int_size:
            print("Index out of bounds")
        else:
            if self.int_size == 1:
                self.first = None
                self.last = None
                self.int_size -= 1
                return
            elif i == 0:
                self.first.next.prev = None
                self.first = self.first.next
                self.int_size -= 1
                return
            elif i == self.int_size - 1:
                self.last.prev.next = None
                self.last = self.last.prev
                self.int_size -= 1
                return
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

            temp_node.prev.next = temp_node.next
            temp_node.next.prev = temp_node.prev

    def clear(self):
        self.first = None
        self.last = None
        self.int_size = 0

    def __str__(self):
        """
        temp_object = self.first
        acum = ''
        while temp_object is not None:
            acum += str(temp_object.node) + " "
            temp_object = temp_object.next
        return acum
        """
        return str(list(self.to_list()))

    def to_list(self):
        temp_object = self.first
        while temp_object is not None:
            yield temp_object.node
            temp_object = temp_object.next

    def __iter__(self):
        return self.to_list()

    def size(self):
        return self.int_size


class ArrayList:

    def __init__(self):
        self.data = []

    def insert_multi(self, *objs):
        for obj in objs:
            self.insert(obj, len(self.data))

    def insert(self, obj, i):
        if i > len(self.data):
            print("Index out of bounds")
        else:
            if i == len(self.data):
                self.data.append(obj)
            else:
                self.data.insert(i, obj)

    def remove(self, obj):
        self.data.remove(obj)

    def get(self, i):
        return self.data[i]

    def size(self):
        return len(self.data)

    def __str__(self):
        acum = "["
        for item in self.data:
            if item is not self.data[len(self.data) - 1]:
                acum += str(item) + ", "
            else:
                acum += str(item) + "]"
        return acum

    def __iter__(self):
        return self.data


class Queue:

    def __init__(self):
        self.ll = LinkedList()

    def push(self, obj):
        self.ll.insert(obj, 0)

    def push_multi(self, *objs):
        for obj in objs:
            self.push(obj)

    def peek(self):
        return self.ll.last

    def pop(self):
        temp_obj = self.ll.last
        self.ll.remove(self.ll.size() - 1)
        return temp_obj

    def size(self):
        return self.ll.size()

    def __str__(self):
        return str(self.ll)


class Stack:

    def __init__(self, size):
        self.max_size = size
        self.ll = LinkedList()

    def push_multi(self, *objs):
        for obj in objs:
            self.ll.insert(obj, 0)

    def push(self, obj):
        if self.ll.size() < self.max_size:
            self.ll.insert(obj, 0)
        else:
            print("Stack overflow")

    def peek(self):
        return self.ll.first.node

    def pop(self):
        temp_object = self.ll.first.node
        self.ll.remove(0)
        return temp_object

    def size(self):
        return self.ll.size()

    def __str__(self):
        return str(self.ll)
