import subprocess
import platform
import time
from DataStructures import NashTable as nt


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
    pipe = "│"
    h_cross = "└"
    cross = "├"

    def __init__(self, name="Output.txt", directory="~/Documents/", teacher=False):
        self.system = platform.system()
        self.name = name
        if not teacher:
            if self.system == "Linux" or self.system == "Darwin":
                process = subprocess.Popen('tree -hua ' + directory + ' > ' + name,
                                           stdout=subprocess.PIPE, shell=True)
                process.communicate()[0].strip()
            self.file = open(name)
        else:
            self.file = open("treeEtc.txt")

    def read_file(self):
        def remove_dir(dir):
            index = 0
            i = 0
            for char in dir:
                if char == "/":
                    index = i
                i += 1
            return dir[:index]

        def separate(string):
            array = string.split("]  ")
            array[0] = array[0].replace(" ", "")
            j = 0
            for char in array[0]:
                if char.isdigit():
                    break
                j += 1

            array[1] = array[1].replace("\n", "")
            if "->" in array[1]:
                array[1] = array[1].split(" -> ")
                return array[1][0], array[0][:j], array[0][j:], array[1][1]
            return array[1], array[0][:j], array[0][j:], ""

        spaces_before = 0  # Know how many spaces were in the line before
        name_before = ""
        file_before = None# The name of the file before
        address = ""  # The directory we are in
        nash = nt()
        dirhands = []
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
                if char == HandlerFiles.h_cross or char == HandlerFiles.cross:
                    # Erase the addresses and pop the directory handlers.
                    found_a_cross = True
                    if spaces < spaces_before:
                        aux = 0
                        to_erase = (spaces_before - spaces)/4
                        while aux < to_erase:
                            address = remove_dir(address)
                            aux += 1
                            dirhands.pop()

                if not found_a_cross and char == " " or char == HandlerFiles.pipe:
                    # Count how many spaces we're in are we in
                    spaces += 1

                if not first_dir and spaces > spaces_before:
                    # Know if the previous file is a folder
                    address += "/" + name_before
                    dirhands.append(nt.Dirhand())
                    file_before["dirhand"] = dirhands[-1]
                    first_dir = True

                if char == "[": # Check if we reach the user and memory part
                    name, owner, size, redir = separate(line[j+1:])
                    break

                j += 1

            if redir == "":
                file = nash.insert(name, address, owner, "", size)
            else:
                file = nash.insert(name, address, owner, "", size, redirects=redir)

            if len(dirhands) > 0:
                dirhands[-1].insert(file)
            # Settings before other iteration
            name_before = name
            spaces_before = spaces
            file_before = file
        return nash


class HandlerUser:

    def __init__(self, dir="~/", teacher=False):
        self.hf = HandlerFiles(directory=dir, teacher=teacher)
        self.nash = self.hf.read_file()

    def run(self):
        print(bcolors.HEADER + bcolors.BOLD + "Welcome!" + bcolors.ENDC)
        i = 0
        while True:
            end_iter = False
            if i != 0:
                print("\n\n")
            else:
                i = 1
            print("======================================================")
            print(bcolors.BOLD + bcolors.OKBLUE + "What operation do you need?", bcolors.ENDC)
            print(bcolors.BOLD + "0. " + bcolors.ENDC + "Quit")
            print(bcolors.BOLD + "1. " + bcolors.ENDC + "Search")
            print(bcolors.BOLD + "2. " + bcolors.ENDC + "Remove")
            decision = input("Type the number of the operation you want: ")
            if not decision.isdigit():
                print(bcolors.FAIL + "The string typed is not a number" + bcolors.ENDC)
                continue
            decision = int(decision)
            if decision == 0:
                return
            elif decision == 1:
                print("Write the name or the initials of the file you want to search; "
                      "if you need it")
                print("to be case sensitive write " + bcolors.UNDERLINE + "(c)"
                      + bcolors.ENDC, "at the start and then "
                                      "write the name of the file you need to search.")
                to_search = input("")
                if len(to_search) >= 3 and to_search[:3] == "(c)":
                    to_search = to_search[3:]
                    files = self.nash.get(to_search)
                else:
                    files = self.nash.get(to_search, False)
                if len(files) == 0:
                    print(bcolors.FAIL + bcolors.UNDERLINE +
                          "Found no files with the name nor the initials given" + bcolors.ENDC)
                    ans = input("\n" + "Want to search the files that "
                                       "have the string in any other place"
                                " rather than the initials? [Y/N] ")
                    if ans.lower().replace(" ", "") == "y":
                        files += self.nash.searchallnash(to_search)
                        if len(files) == 0:
                            print(bcolors.FAIL + bcolors.UNDERLINE +
                                  "Found no files with the name nor the initials given"
                                  + bcolors.ENDC)
                            continue
                    else:
                        continue

                HandlerUser.print_files(files)

                while True:
                    ans2 = input(bcolors.BOLD + "Did you find the file you wanted?" +
                                 bcolors.ENDC + "[Y/N] ")
                    if ans2.lower().replace(" ","") == "n":
                        ans3 = input("\n" + "Want to search the files that have the string "
                                            "in any other place"
                                            " rather than the initials? [Y/N] ")
                        if ans3.replace(" ", "").lower() == "y":
                            files = self.nash.searchallnash(to_search)
                            if len(files) == 0:
                                print(bcolors.FAIL + bcolors.UNDERLINE +
                                      "Found no files with the name nor the initials given"
                                      + bcolors.ENDC)
                                break
                            else:
                                HandlerUser.print_files(files)
                        else:
                            break

                    answer = input(bcolors.OKBLUE + "Do you want to know the address "
                                                    "of a file? "
                                                    "[Y/N] " + bcolors.ENDC)
                    if answer.lower().replace(" ", "") == "y":
                        while True:
                            print("\n")
                            index = input(bcolors.OKBLUE + "Type the index of the file that you "
                                                           "want to know the address"
                                          + bcolors.ENDC + "(Enter 0 to cancel) ")

                            if not index.isdigit():
                                print(bcolors.WARNING + "That index doesn't exists"
                                      + bcolors.ENDC)
                                continue

                            index = int(index)
                            if index == 0:
                                break
                            if index > len(files):
                                print(bcolors.FAIL + "There's no file with that index!"
                                      + bcolors.ENDC)
                            else:
                                print("Address:", files[index - 1]["dir"])
                    while True:
                        ans4 = input(bcolors.BOLD + "Do you want to know the content "
                                                    "of a folder? "
                                                    "[Y/N] " + bcolors.ENDC).lower()
                        if ans4 == "y":
                            print("\n\n")
                            index = input(bcolors.OKBLUE + "Type the index of the "
                                                           "file that you want to "
                                                           "know it's subdirectories "
                                                           "(Type 0 to cancel) "
                                          + bcolors.ENDC)

                            if not index.isdigit():
                                print(bcolors.WARNING + "That index doesn't exists"
                                      + bcolors.ENDC)
                                continue

                            index = int(index) - 1
                            if index == -1:
                                end_iter = True
                                break
                            elif index >= len(files):
                                print(bcolors.FAIL + "That index doesn't exist" + bcolors.ENDC)
                                continue
                            file = files[index]
                            if "dirhand" in file:
                                files = file["dirhand"].sub
                                if len(files) == 0 or files[0] == file:
                                    print(bcolors.FAIL + bcolors.UNDERLINE +
                                          "Found no files with the name nor the initials given"
                                          + bcolors.ENDC)
                                    continue

                                HandlerUser.print_files(file["dirhand"].sub)
                                break
                            else:
                                print(bcolors.FAIL + "The file selected is "
                                                     "not a directory or it's empty"
                                      + bcolors.ENDC)
                                end_iter = True
                                break
                        else:
                            end_iter = True
                            break
                    if end_iter:
                        break
            elif decision == 2:
                print("Write the name or the initials of the file you want to delete; "
                      "if you need the search")
                print("to be case sensitive write " + bcolors.UNDERLINE + "(c)"
                      + bcolors.ENDC, "at the start and then "
                                      "write the name of the file you need to remove.")
                to_search = input("")
                if len(to_search) >= 3 and to_search[:3] == "(c)":
                    to_search = to_search[3:]
                    files = self.nash.get(to_search)
                else:
                    files = self.nash.get(to_search, False)
                if len(files) == 0:
                    print(bcolors.FAIL + bcolors.UNDERLINE +
                          "Found no files with the name nor the initials given" + bcolors.ENDC)
                    ans = input("\n" + "Want to search the files that "
                                       "have the string in any other place"
                                       " rather than the initials? [Y/N] ")
                    if ans.lower().replace(" ", "") == "y":
                        files += self.nash.searchallnash(to_search)
                        if len(files) == 0:
                            print(bcolors.FAIL + bcolors.UNDERLINE +
                                  "Found no files with the name nor the initials given"
                                  + bcolors.ENDC)
                            continue
                    else:
                        continue

                HandlerUser.print_files(files)
                ans5 = input(bcolors.BOLD + "Do you want to know more "
                                            "information about the files found?"
                             "[Y/N] " + bcolors.ENDC).lower()
                if ans5 == "y":
                    answer = input(bcolors.OKBLUE + "Do you want to know the address "
                                                    "of a file? "
                                                    "[Y/N] " + bcolors.ENDC)
                    if answer.lower().replace(" ", "") == "y":
                        while True:
                            print("\n")
                            index = input(bcolors.OKBLUE + "What address do you want to know? "
                                          + bcolors.ENDC + "(Enter 0 to cancel) ")

                            if not index.isdigit():
                                print(bcolors.WARNING + "That index doesn't exists"
                                      + bcolors.ENDC)
                                continue

                            index = int(index)
                            if index == 0:
                                break
                            if index > len(files):
                                print(bcolors.FAIL + "There's no file with that index!"
                                      + bcolors.ENDC)
                            else:
                                print("Address:", files[index - 1]["dir"])

                while True:
                    ans6 = input("\n\n" + bcolors.BOLD + "Type the index of the file "
                                                       "you want to remove: "
                                 "(type 0 to cancel) " + bcolors.ENDC)
                    if not ans6.isdigit():
                        print(bcolors.WARNING + "The string written is not a digit"
                              + bcolors.ENDC)
                        continue

                    ans6 = int(ans6) - 1
                    if ans6 == -1:
                        break

                    if ans6 >= len(files):
                        print(bcolors.WARNING + "Such index doesn't exist"
                              + bcolors.ENDC)

                    file = files[ans6]
                    print("\n" + bcolors.FAIL + "Are you sure you want to delete:" )
                    print(bcolors. BOLD + "\t[ " + file["owner"] + " " + file["size"] + " " +
                          file["date"] + "] " + file["name"] + " at " + file["dir"]
                          + "? " + bcolors.ENDC)
                    ans7 = input(bcolors.FAIL + "It will not be send to the trash and it's "
                                                "an action you can't undo [Y/N] "
                                 + bcolors.ENDC).lower()
                    if ans7 == "y":
                        print("\n" + bcolors.BOLD + "Removing", file["name"] + "..." +
                              bcolors.ENDC)
                        self.nash.remove(file["name"], file)
                        path = file["dir"] + "/" + file["name"]
                        action = "rm "
                        if "dirhand" in file:
                            action += "-r "
                        process = subprocess.Popen(action + path,
                                                   stdout=subprocess.PIPE, shell=True)
                        process.communicate()[0].strip()
                        print(bcolors.OKGREEN + "Removed succesfully " + file["name"] +  "!"
                              + bcolors.ENDC)
                        break
                    else:
                        break

    @staticmethod
    def print_files(my_list):
        index = 1
        my_dict = {}
        for item in my_list:
            my_tuple = (item["name"], item["size"], item["owner"])
            if my_tuple not in my_dict or my_dict[my_tuple] != item:
                try:
                    print(bcolors.BOLD + str(index) + bcolors.ENDC + "." + "[" + item["owner"],
                          item["size"], item["date"] + "]", item["name"], "->",
                          item["redirects"])
                except KeyError:
                    print(bcolors.BOLD + str(index) + bcolors.ENDC + "." + "[" + item["owner"],
                          item["size"], item["date"] + "]", item["name"])

                my_dict[my_tuple] = item
                index += 1

        print(bcolors.OKGREEN + "Found", str(index-1) + " files!\n" + bcolors.ENDC)


hu = HandlerUser()
hu.run()
