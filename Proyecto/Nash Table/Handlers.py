import subprocess
import platform
import time
import importlib.util as ut
spec = ut.spec_from_file_location("Nash Tables",
                                  "/home/juanse/Documents/JuanSePlazas/Proyecto/Nash\ Table/DataStructures.py")
nt = ut.module_from_spec(spec)
spec.loader.exec_module(nt)
nt.MyClass()



class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    WARNING = '\033[93m'
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    UNDERLINE = '\033[4m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'


class HandlerFiles:

    def __init__(self, name="Output.txt", directory="~/", teacher=False):
        """
        :param name: the name of the file to read
        :param directory: the directory to begin the tree
        :param teacher: if the teacher wants to use the treeEtc.txt
        """
        self.system = platform.system()
        self.name = name
        if not teacher:
            if self.system == "Linux" or self.system == "Darwin":
                process = subprocess.Popen('tree -hua ' + directory + ' > ' + name, stdout=subprocess.PIPE, shell=True)
                process.communicate()[0].strip()
            self.file = open(name)
        else:
            self.file = open("treeEtc.txt")

    def read_file(self):
        """
        :return: a nash table with the files of the tree
        """
        pipe = "│"
        h_cross = "└"
        cross = "├"

        def remove_dir(dir):
            index = 0
            i = 0
            for char in dir:
                if char == "/":
                    index = i
                i += 1
            return dir[:index]

        def separate(string):
            string = string.replace(" ", "")
            array = string.split("]")
            j = 0
            for char in array[0]:
                if char.isdigit():
                    break
                j += 1

            array[1] = array[1].replace("\n", "")
            if "->" in array[1]:
                array[1].split("->")
                return array[1][0], array[0][:j], array[0][j:], array[1][1]
            return array[1], array[0][:j], array[0][j:], ""

        spaces_before = 0  # Know how many spaces were in the line before
        name_before = ""  # The name of the file before
        address = ""  # The directory we are in
        nash = nt()
        i = 0
        for line in self.file:
            # So he can add the first direction
            if i == 0:
                address += line.replace("\n", "")
                if address[-1] == "/":
                    address = address[:-1]
                i = 1
                continue

            spaces = 0
            name = ""
            j = 0  # Index of the char we are
            found_a_cross = False
            first_dir = False
            redir = ""
            for char in line:
                if char == h_cross or char == cross:
                    found_a_cross = True
                    if spaces < spaces_before:
                        aux = 0
                        to_erase = (spaces_before - spaces)/4
                        while aux < to_erase:
                            address = remove_dir(address)
                            aux += 1
                if not found_a_cross and char == " " or char == pipe:
                    # Count how many spaces we're in are we in
                    spaces += 1

                if not first_dir and spaces > spaces_before:
                    address += "/" + name_before
                    first_dir = True

                if char == "[": # Check if we reach the user and memory part
                    name, owner, size, redir = separate(line[j+1:])
                    break

                j += 1

            if redir == "":
                nash.insert(name, address, owner, "", size)
            else:
                nash.insert(name, address, owner, "", size, redirects=redir)

            # Settings before other iteration
            name_before = name
            spaces_before = spaces
        return nash


class HandlerUser:

    def __init__(self):
        self.hf = HandlerFiles()
        self.nash = self.hf.read_file()

    def run(self):
        print(bcolors.HEADER + bcolors.BOLD + "Welcome!" + bcolors.ENDC)
        i = 0
        while True:
            if i != 0:
                print("\n\n")
            else:
                i = 1
            print("======================================================")
            print(bcolors.BOLD + bcolors.OKBLUE + "What operation do you need?", bcolors.ENDC)
            print(bcolors.BOLD + "0. " + bcolors.ENDC + "Quit")
            print(bcolors.BOLD + "1. " + bcolors.ENDC + "Search")
            print(bcolors.BOLD + "2. " + bcolors.ENDC + "Remove")
            decision = int(input("Press the number wanted: "))
            if decision == 0:
                return
            elif decision == 1:
                print("Write the name or the initials of the file you want to search; if you need it")
                print("to be case sensitive write " + bcolors.UNDERLINE + "(c)"
                      + bcolors.ENDC, "and then write the file you need to search.")
                to_search = input("")
                if len(to_search) >= 3 and to_search[:3] == "(c)":
                    to_search = to_search[3:]
                    files = self.nash.get(to_search)
                else:
                    files = self.nash.get(to_search, False)
                if len(files) == 0:
                    print(bcolors.FAIL + bcolors.UNDERLINE +
                          "Found no files with the name nor the initials given" + bcolors.ENDC)
                    ans = input("\n" + "Want to search the files that have the string in any other place"
                                " rather than the initials? [Y/N] ")
                    if ans.lower().replace(" ", "") == "y":
                        files += self.nash.searchallnash(to_search)
                        if len(files) == 0:
                            print(bcolors.FAIL + bcolors.UNDERLINE +
                                  "Found no files with the name nor the initials given" + bcolors.ENDC)
                            continue
                    else:
                        continue

                HandlerUser.print_files(files)

                ans2 = input(bcolors.BOLD + "Did you find the file you wanted?" + bcolors.ENDC + "[Y/N] ")
                if ans2.lower().replace(" ","") == "n":
                    ans3 = input("\n" + "Want to search the files that have the string in any other place"
                                        " rather than the initials? [Y/N] ")
                    if ans3.replace(" ", "").lower() == "y":
                        files = self.nash.searchallnash(to_search)
                        if len(files) == 0:
                            print(bcolors.FAIL + bcolors.UNDERLINE +
                                  "Found no files with the name nor the initials given" + bcolors.ENDC)
                            continue
                        else:
                            HandlerUser.print_files(files)
                    else:
                        continue

                answer = input(bcolors.OKBLUE + "Do you want to know the address of a file? [Y/N] " + bcolors.ENDC)
                if answer.lower().replace(" ", "") == "y":
                    while True:
                        print("\n")
                        index = input(bcolors.OKBLUE + "What address do you want to know? "
                                      + bcolors.ENDC + "(Enter 0 to cancel) ")

                        if not index.isdigit():
                            print(bcolors.WARNING + "That index doesn't exists" + bcolors.ENDC)
                            continue

                        index = int(index)
                        if index == 0:
                            break
                        if index > len(files):
                            print(bcolors.FAIL + "There's no file with that index!" + bcolors.ENDC)
                        else:
                            print("Address:", files[index - 1]["dir"])

    @staticmethod
    def print_files(my_list):
        index = 1
        for item in my_list:
            try:
                print(bcolors.BOLD + str(index) + bcolors.ENDC + "." + "[" + item["owner"], item["size"],
                      item["date"] + "]", item["name"], "->", item["redirects"])
            except KeyError:
                print(bcolors.BOLD + str(index) + bcolors.ENDC + "." + "[" + item["owner"], item["size"],
                      item["date"] + "]", item["name"])
            index += 1

        print(bcolors.OKGREEN + "Found", str(index-1) + " files!\n" + bcolors.ENDC)


class Tester:
    def __init__(self):
        self.hf = HandlerFiles(teacher=True)
        self.file = open('Times.csv', 'w')
        self.nt = nt()

    def read_file_times(self):
        self.file.write("Reading file: (seconds *10⁶) \n")
        max = 0
        min = 0
        avg = 0
        for i in range(100):
            before = time.clock()*1000000
            self.nt = self.hf.read_file()
            now = time.clock()*1000000

            delta = now - before
            if i == 0:
                max = delta
                min = delta
            else:
                if max < delta:
                    max = delta
                elif min > delta:
                    min = delta
            avg += delta
            self.file.write(str(delta) + "\n")
            self.hf = HandlerFiles(teacher=True)

        self.file.write("Average," + str(avg / 100) + "\n")
        self.file.write("Max," + str(max) + "\n")
        self.file.write("Min," + str(min) + "\n")

    def insert_times(self):
        self.file.write("Insertion: (seconds *10⁶) \n")
        max = 0
        min = 0
        avg = 0
        for i in range(100):
            before = time.clock() * 1000000
            self.nt.insert("sdagnjgnahg jewkewkj.pyjj", "", "", "", "")
            now = time.clock() * 1000000

            delta = now - before
            if i == 0:
                max = delta
                min = delta
            else:
                if max < delta:
                    max = delta
                elif min > delta:
                    min = delta
            avg += delta
            self.file.write(str(delta) + "\n")

        self.file.write("Average," + str(avg / 100) + "\n")
        self.file.write("Max," + str(max) + "\n")
        self.file.write("Min," + str(min) + "\n")

    def get_times(self):
        self.file.write("Get: (seconds *10⁶) \n")
        max = 0
        min = 0
        avg = 0
        for i in range(100):
            before = time.clock() * 1000000
            self.nt.get("Python.py")
            now = time.clock() * 1000000

            delta = now - before
            if i == 0:
                max = delta
                min = delta
            else:
                if max < delta:
                    max = delta
                elif min > delta:
                    min = delta
            avg += delta
            self.file.write(str(delta) + "\n")

        self.file.write("Average," + str(avg / 100) + "\n")
        self.file.write("Max," + str(max) + "\n")
        self.file.write("Min," + str(min) + "\n")

    def remove_times(self):
        self.file.write("Insertion: (seconds *10⁶) \n")
        max = 0
        min = 0
        avg = 0
        for i in range(100):
            before = time.clock() * 1000000
            self.nt.insert("sdagnjgnahg jewkewkj.pyjj", "", "", "", "")
            now = time.clock() * 1000000

            delta = now - before
            if i == 0:
                max = delta
                min = delta
            else:
                if max < delta:
                    max = delta
                elif min > delta:
                    min = delta
            avg += delta
            self.file.write(str(delta) + "\n")

        self.file.write("Average," + str(avg / 100) + "\n")
        self.file.write("Max," + str(max) + "\n")
        self.file.write("Min," + str(min) + "\n")


hu = HandlerUser()
test = Tester()
test.read_file_times()
test.insert_times()
test.get_times()
test.remove_times()