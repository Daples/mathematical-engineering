class LinkedList:

    class Node:
        def __init__(self, node):
            self.node = node
            self.next = None
            self.prev = None

    def __init__(self):
        self.first = None
        self.size = 0
        self.last = None

    def insert(self, obj, i):
        if i > self.size:
            print("Index out of bounds")
        else:
            obj_node = LinkedList.Node(obj)
            if self.size < 4 or i < int(self.size/2):
                mov_obj = self.first
                if mov_obj is not None:
                    for j in range(i):
                        mov_obj = mov_obj.next
                else:
                    self.first = obj_node
                    self.last = obj_node
                    self.size += 1
                    return
            else:
                mov_obj = self.last
                j = self.size - 1
                while j > i:
                    mov_obj = mov_obj.prev
                    j -= 1

            obj_node.next = mov_obj
            obj_node.prev = mov_obj.prev
            mov_obj.prev = obj_node
            mov_obj.prev.next = obj_node

            if self.last.next is not None:
                temp_last = self.last
                while temp_last.next is not None:
                    temp_last = temp_last.next
                self.last = temp_last

            self.size += 1


lin = LinkedList()
lin.insert(3,0)
lin.insert(4,0)

temp = lin.first
while temp.next is not None:
    print(str(temp))
    temp = temp.next

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

