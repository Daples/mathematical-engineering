class LinkedList(object):

    class Node(object):
        def __init__(self, node):
            """
            :param node: It's the value that the node will hold
            """
            self.node = node
            self.next = None
            self.prev = None

        def set_next(self, obj):
            """
            :param obj: The object to set the next
            :return: Nothing
            """
            self.next = obj

        def set_prev(self, obj):
            """
            :param obj: The object to set the previous
            :return:
            """
            self.prev = obj

        def set(self, node):
            """
            :param node: Set the instance to the node passed
            :return: Nothing
            """
            self.node = node.node
            self.set_next(node.get_next())
            self.set_prev(node.get_prev())

        def get_prev(self):
            """
            :return: the previous object
            """
            return self.prev

        def get_next(self):
            """
            :return: the next object
            """
            return self.next

        def __str__(self):
            """
            :return: the string version of the Node
            """
            return str(self.node)

    def __init__(self):
        self.first = None
        self.int_size = 0
        self.last = None

    def __len__(self):
        """
        :return: the size of the list
        """
        return self.int_size

    def insert_multi(self, *objs):
        """
        :param objs: the objects to add to the list
        :return: Nothing
        """
        for obj in objs:
            self.insert(obj, self.int_size)

    def insert(self, obj, i=0):
        """
        :param obj: the object to insert
        :param i: the index to insert the object
        :return: nothing
        """
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
        """
        :param i: the index to search for
        :return: The node of the node in that index
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
        :param i: the index of the object to remove
        :return: nothing
        """
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
        """
        :return: it empties the list
        """
        self.first = None
        self.last = None
        self.int_size = 0

    def __str__(self):
        """
        :return: the list represented in a string
        """
        temp_object = self.first
        acum = ''
        while temp_object is not None:
            if temp_object is not self.last:
                acum += str(temp_object.node) + " <-> "
            else:
                acum += str(temp_object.node)
            temp_object = temp_object.next
        return acum

    def __contains__(self, item):
        """
        :param item: the item to search in the list
        :return: if the item is in the list
        """
        for i in self:
            if i is item:
                return True
        return False

    def to_list(self):
        """
        :return: it converts the linked list to a python list
        """
        temp_object = self.first
        while temp_object is not None:
            yield temp_object.node
            temp_object = temp_object.next

    def __iter__(self):
        """
        :return: the linked list in a list
        """
        return self.to_list()

    def size(self):
        """
        :return: the size of the list
        """
        return self.int_size

    def get_first(self):
        """
        :return: the first item in the list
        """
        return self.first

    def get_last(self):
        """
        :return: the last item in the lost
        """
        return self.last


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

    class Dirhand:
        def __init__(self):
            self.sub = []

        def insert(self, file):
            self.sub.append(file)

        def __iter__(self):
            return self.sub

        def __str__(self):
            return str(self.sub)

    def __init__(self, depth=260, __level__=1):
        """
        :param depth: the depth of the trie
        :param __level__: the size of the strings that the nash holds
        """
        self.depth = depth
        self.hash = {}
        self.level = __level__
        self.size = 0

    def __str__(self):
        """
        :return: A string version of the string
        """
        return str(self.hash)

    def __len__(self):
        """
        :return: the size of the nash table
        """
        return self.size

    def __contains__(self, item):
        """
        :param item: a key
        :return: if the key is in the hash table of the nash table
        """
        return item in self.hash

    def getdepth(self):
        """
        :return: the real depth of the table
        """
        return self.depth + 1

    def insert(self, name, dir, own, date, size, **kwargs):
        """
        :param name: the name of the file
        :param dir: the directory that the file is located
        :param own: the owner of the file
        :param date: the date of the file
        :param size: the size of the file
        :param kwargs: the extra arguments that the file has
        :return: the file itself
        """
        file = {"name": name, "dir": dir, "owner": own, "date": date, "size": size}
        for key in kwargs:
            if key not in file:
                file[key] = kwargs[key]
        if name == "":
            self.hash[""] = NashTable.Branch(depth=self.depth-1)
            self.hash[""].table.insert(file, self.hash[""].table.size())
        else:
            self.__aux__insert__(0, file)
        self.size += 1
        return file

    def __aux__insert__(self, letter_index, item):
        """
        :param letter_index: the letter we are on
        :param item: the file you want to insert
        :return: nothing
        """
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
        """
        :param name: the name of the file
        :param case_sens: if the search is case sensitive or not
        :return: a list with the files found
        """
        if name == "":
            return
        if case_sens:
            return self.__aux__get__(name, 0)
        else:
            return self.__aux__get__case(name, 0)

    def __aux__get__(self, name, letter_index):
        """
        It searches with the name given case sensitive
        :param name: the name to search
        :param letter_index: the letter we are in
        :return: a list with the files found
        """
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
        """
        It searches for the files with the name given not being case sensitive
        :param name: the name of the file you're searching
        :param letter_index: the letter we're in
        :return: a list with the files found
        """
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
                if branch.nash is not None:
                    temp = branch.nash.__aux__get__case(name, letter_index + 1)
                else:
                    temp = []

            if temp is not None:
                total += temp

        return total

    def remove(self, name, file):
        """
        It removes the file from the nash table and the directory it's in
        :param name: the name you want to remove
        :param file: a reference to the file you want to delete
        :return: nothing
        """
        if name == "":
            if "" in self:
                self.hash[""].table.remove(0)
            return

        letter_index = 0
        mov_nash = self
        letter = name[letter_index]
        while len(name) != mov_nash.level and mov_nash.getdepth() != 0:
            if mov_nash is None:
                break
            if letter in mov_nash:
                mov_nash = mov_nash.hash[letter].nash
            else:
                return
            letter_index += 1
            letter = name[letter_index]

        index = 0
        for item in mov_nash.hash[letter].table:
            if item["name"] == name and item == file:
                mov_nash.hash[letter].table.remove(index)
                break
            index += 1

        father = file["dir"].split("/")[-1]
        files = self.get(father)
        for item in files:
            if "dirhand" in item:
                for subdir in item["dirhand"].sub:
                    if file == subdir:
                        item["dirhand"].sub.remove(subdir)
                        return

    def __search__all__(self, name):
        """
        It searches all the depths of a nash
        :param name: the name you're searching for
        :return: a list with the files found
        """
        files = []
        for key in self.hash:
            branch = self.hash[key]
            files += branch.table
            if branch.nash is not None:
                files += branch.nash.__search__all__(name)

        return files

    def searchallnash(self, name):
        """
        It searches all the nash table for files with a name
        :param name: the name you're searching for
        :return: a list with the files found
        """
        files = []
        for key in self.hash:
            branch = self.hash[key]
            for item in branch.table:
                if not item["name"].startswith(name) and name in item["name"]:
                    files.append(item)

            if branch.nash is not None:
                files += branch.nash.searchallnash(name)

        return files
