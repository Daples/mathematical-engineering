class LinkedList:

    class Node:
        def __init__(self, node):
            self.node = node
            self.next = None
            self.prev = None

        def __str__(self):
            return str(self.node)

    def __init__(self):
        self.first = None
        self.size = 0
        self.last = None

    def insert_multi(self, *objs):
        for obj in objs:
            self.insert(obj, self.size)

    def insert(self, obj, i=0):
        if i > self.size:
            print("Index out of bounds")
        else:
            obj_node = LinkedList.Node(obj)
            mov_obj = self.first
            if mov_obj is None:
                self.first = obj_node
                self.last = obj_node
                self.size += 1
                return
            elif i == self.size:
                obj_node.prev = self.last
                self.last.next = obj_node
                self.last = obj_node
                self.size += 1
                return
            elif self.size < 4 or i < int(self.size / 2):
                for j in range(i):
                    mov_obj = mov_obj.next
            else:
                j = self.size - 1
                while j > i:
                    mov_obj = mov_obj.prev
                    j -= 1

            obj_node.next = mov_obj
            obj_node.prev = mov_obj.prev
            mov_obj.prev = obj_node
            mov_obj.prev.next = obj_node

            self.size += 1

    def get(self, i):
        if i >= self.size:
            print("The index passed doesn't exist on the list")
            return None
        else:
            if i > self.size/2:
                j = self.size - 1
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
        if i >= self.size:
            print("Index out of bounds")
        else:
            if self.size == 1:
                self.first = None
                self.last = None
                self.size -= 1
                return
            elif i == 0:
                self.first.next.prev = None
                self.first = self.first.next
                self.size -= 1
                return
            elif i == self.size - 1:
                self.last.prev.next = None
                self.last = self.last.prev
                self.size -= 1
                return
            elif i > self.size/2:
                temp_node = self.last
                j = self.size - 1
                while j > i:
                    temp_node = temp_node.prev
                    j -= 1
            else:
                temp_node = self.first
                for j in range(i):
                    temp_node = temp_node.next

            temp_node.prev.next = temp_node.next
            temp_node.next.prev = temp_node.prev



    def __str__(self):
        temp_object = self.first
        acum = ''
        while temp_object is not None:
            acum += str(temp_object.node) + " "
            temp_object = temp_object.next
        return acum

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

    def __str__(self):
        return str(self.data)