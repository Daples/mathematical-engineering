class LinkedList(object):

    class Node(object):
        def __init__(self, node):
            self.node = node
            self.next = None
            self.prev = None

        def set_next(self, obj):
            self.next = obj

        def set_prev(self, obj):
            self.prev = obj

        def set(self, node):
            self.node = node.node
            self.set_next(node.get_next())
            self.set_prev(node.get_prev())

        def get_prev(self):
            return self.prev

        def get_next(self):
            return self.next

        def __str__(self):
            return str(self.node)

    def __init__(self):
        self.first = None
        self.int_size = 0
        self.last = None

    def __len__(self):
        return self.int_size

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

            return temp_node.node

    def get_iterator(self):
        return self.it

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

    def __contains__(self, item):
        for i in self:
            if i is item:
                return True
        return False

    def to_list(self):
        temp_object = self.first
        while temp_object is not None:
            yield temp_object.node
            temp_object = temp_object.next

    def __iter__(self):
        return self.to_list()

    def size(self):
        return self.int_size

    def get_first(self):
        return self.first

    def get_last(self):
        return self.last


class ArrayList:

    def __init__(self):
        self.data = []

    def __len__(self):
        return len(self.data)

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
        return str(self.data)

    def __iter__(self):
        return self.data

    def __contains__(self, item):
        return item in self.data


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


class HashTable:
    def __init__(self, size=100):
        self.size = size
        self.table = [None for e in range(size)]

    def _hash_function(self, key):
        if type(key) == str:
            acum = 0
            i = 1
            n = len(key)
            for let in key:
                acum += ord(let)*(31**(n - i))
                i += 1
            return acum % self.size
        else:
            print("The key passed is not a string")

    def add(self, keys):
        for key in keys:
            hash_value = self._hash_function(key["key"])
            if self.table[hash_value] is None:
                self.table[hash_value] = []
            self.table[hash_value].append(key["value"])

    def get(self, key):
        hash_value = self._hash_function(key)
        if self.table[hash_value] is None:
            print("There's no value assinged to that key")
            return None
        else:
            if len(self.table[hash_value]) == 1:
                return self.table[hash_value][0]
            else:
                return self.table[hash_value]

    # 4
    def is_key(self, key):
        if self.get(key) is None:
            return False
        else:
            return True

    # 5
    def is_value(self, value):
        for i in range(self.size):
            if self.table[i] is not None:
                for j in range(len(self.table[i])):
                    if self.table[i][j] == value:
                        return True

        return False


class NashTable:

    class Branch(object):
        def __init__(self, depth):
            self.nash = None
            self.depth = depth
            self.table = LinkedList()

        def __init_nash__(self, level):
            self.nash = NashTable(self.depth, level)

        def __str__(self):
            return "(" + str(self.table) + ",", str(self.nash) + ")"

    def __init__(self, depth=2, level=1):
        self.depth = depth
        self.hash = {}
        self.level = level
        self.size = 0

    def __str__(self):
        return str(self.hash)

    def __len__(self):
        return self.size

    def __contains__(self, item):
        return item in self.hash

    def getdepth(self):
        return self.depth + 1

    def insert(self, name, dir, own, date, size, **kwargs):
        file = {"name": name, "dir": dir, "owner": own, "date": date, "size": size}
        for key in kwargs:
            if key not in file:
                file[key] = kwargs[key]
        if name == "":
            self.hash[""] = NashTable.Branch(depth=self.depth-1)
            self.hash[""].table.insert(file, self.hash[""].table.size())
            return
        self.__aux__insert__(0, file)
        self.size += 1

    def __aux__insert__(self, letter_index, item):
        letter = item["name"][letter_index]
        if letter not in self.hash:
            self.hash[letter] = NashTable.Branch(depth=self.depth-1)
        if self.getdepth() == 0 or len(item["name"]) == self.level:
            my_list = self.hash[letter].table
            my_list.insert(item, my_list.size())
        else:
            if self.hash[letter].nash is None:
                self.hash[letter].__init_nash__(self.level+1)
            self.hash[letter].nash.__aux__insert__(letter_index+1, item)

    def get(self, name, case_sens=True):
        if name == "":
            return
        if case_sens:
            return self.__aux__get__(name, 0)
        else:
            return self.__aux__get__case(name, 0)

    def __aux__get__(self, name, letter_index):
        letter = name[letter_index]
        if letter in self.hash:
            branch = self.hash[letter]
        else:
            return []
        if self.getdepth() == 0 or len(name) == self.level:
            ll = branch.table
            files = []
            if self.getdepth() != 0 and branch.nash is not None:
                files += branch.nash.__search__all__(name)
            for item in ll:
                if name in item["name"]:
                    files.append(item)
            return files
        else:
            return branch.nash.__aux__get__(name, letter_index+1)

    def __aux__get__case(self, name, letter_index):
        letter = name[letter_index]
        total = []
        temp = []
        if letter.upper() not in self and letter.lower() not in self:
            return []
        letters = []
        if letter.upper() in self:
            letters.append(letter.upper())
        if letter.lower() in self:
            letters.append(letter.lower())

        for let in letters:
            branch = self.hash[let]
            if self.getdepth() == 0 or len(name) == self.level:
                ll = branch.table
                files = []
                if self.getdepth() != 0 and branch.nash is not None:
                    files += branch.nash.__search__all__(name)
                for item in ll:
                    if name.lower() in item["name"].lower() and item not in files:
                        files.append(item)
                total += files
            else:
                temp = branch.nash.__aux__get__case(name, letter_index + 1)

            if temp is not None:
                total += temp

        return total

    def __search__all__(self, name):
        files = []
        for key in self.hash:
            branch = self.hash[key]
            files += branch.table
            if branch.nash is not None:
                files += branch.nash.__search__all__(name)

        return files

    def searchallnash(self, name):
        files = []
        for key in self.hash:
            branch = self.hash[key]
            for item in branch.table:
                if not item["name"].startswith(name) and name in item["name"]:
                    files.append(item)

            if branch.nash is not None:
                files += branch.nash.searchallnash(name)

        return files
