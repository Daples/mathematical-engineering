import re
import pyperclip


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Machine:
    sign = {0: -1, 1: 1}
    sign_string = {0: "-", 1: "+"}
    er = "e"
    suc = "s"
    width = 800

    def __init__(self, n, nm):
        self.n = n
        self.nm = nm
        self.exp = ""
        self.m = ""
        self.sm = 0
        self.se = 0

    def get_ne(self):
        return self.n - self.nm - 2

    def set_machine(self, n, nm):
        self.n = n
        self.nm = nm
        self.exp = ""
        self.m = ""
        self.sm = 0
        self.se = 0

    def mach2dec(self, num):
        def bin2dec(n_machine):
            try:
                num1 = n_machine[3:4 + self.nm]
                exp = n_machine[5 + self.nm:]
                int_exp = int(exp, 2)
                sign = n_machine[4 + self.nm]

                if sign == "+":
                    zeros = ""
                    if int_exp >= len(num1):
                        for i in range(int_exp - len(num1)):
                            zeros += "0"
                    else:
                        zeros = ""
                    num1 = num1[0:int_exp] + zeros + "." + num1[int_exp:]
                else:
                    zeros = ""
                    for i in range(int_exp):
                        zeros += "0"
                    num1 = "0." + zeros + num1

                str_num = str(num1)
                aux = str_num.split(".")
                integer = aux[0]
                dec = []
                if len(aux) == 2:
                    dec = aux[1]

                integer = int(integer, 2)

                i = 1
                dec_final = 0
                while i < len(dec) + 1:
                    dec_final += int(dec[i - 1]) * 2 ** (-1 * i)
                    i = i + 1

                ans = float(integer + dec_final)
                if n_machine[0] == "-":
                    ans *= -1

                return ans, Machine.suc
            except OverflowError:
                print(Colors.FAIL +
                      "The number that is being calculated is higher "
                      "than the biggest number of your computer." +
                      Colors.END)
                return 0, Machine.er

        if len(num) != self.n:
            print(Colors.FAIL +
                  "Error, please check if the number passed is the same "
                  "number as the bits of the machine." +
                  Colors.END)
            return 0, Machine.er
        elif not re.fullmatch("[01]+", num):
            print(Colors.FAIL +
                  "Error, the number you passed is not a valid "
                  "machine number." +
                  Colors.END)
            return 0, Machine.er

        self.sm = int(num[0])
        self.m = num[1:1 + self.nm]
        self.se = int(num[1 + self.nm])
        self.exp = num[2 + self.nm:]

        num1 = Machine.sign_string[self.sm] + "0.1" + self.m + Machine.sign_string[self.se] + self.exp

        ans = bin2dec(num1)
        return ans

    def dec2mach(self, num):
        def get_info_dec(dec):
            def purify_exp(num1):
                exp1 = num1[2:]
                string = ""
                for z in range(self.get_ne() - len(exp1)):
                    string += "0"
                return string + exp1

            if dec == 0:
                return "0"
            if dec > 0:
                sm = 1
            else:
                sm = 0
                dec = -1 * dec

            binint = ""
            int1 = int(dec)
            if int1 == 1:
                one = True
            else:
                one = False
            fr = dec - int1

            if int1 != 0:
                while int1:
                    rem = int1 % 2
                    int1 //= 2
                    binint += str(rem)

            binint = binint[:: -1]
            first = binint.find("1")
            binint = binint[first + 1:]
            exp = len(binint) + 1

            if exp - 1 < self.nm and fr != 0:
                if exp - 1 != 0 or one:
                    i = 0
                    bin_fr = ""
                    while self.nm - exp - i + 1:
                        fr *= 2
                        bit = int(fr)
                        bin_fr += str(bit)
                        fr = fr - bit
                        i += 1

                    exp = purify_exp(bin(exp))
                    return str(sm) + binint + bin_fr + "1" + exp
                else:
                    exp = 0
                    i = 0
                    bin_fr = ""
                    first1 = False
                    while self.nm - i:
                        fr *= 2
                        bit = int(fr)
                        fr = fr - bit
                        if not first1:
                            if not bit:
                                exp += 1
                            first1 = bit
                        else:
                            bin_fr += str(bit)
                            i += 1

                    exp = purify_exp(bin(exp))
                    return str(sm) + bin_fr + "0" + exp
            else:
                extra = ""
                for k in range(self.nm - exp + 1):
                    extra += "0"
                exp = purify_exp(bin(exp))
                return str(sm) + binint[0:self.nm] + extra + "1" + exp

        try:
            num = float(num)
        except ValueError:
            print(Colors.FAIL + "The input passed is not a numeric value." + Colors.END)
            return 0, Machine.er

        maq = get_info_dec(num)
        ans = maq
        return ans, Machine.suc

    def epsilon(self):
        ep = (2 ** -(self.nm))

        if ep == 0:
            print(Colors.FAIL + "The epsilon of the machine is smaller than the smallest number of your computer, "
                                "therefore it cannot be calculated." + Colors.END)

        return ep, Machine.suc

    def biggest_number(self):
        mach = ""
        for i in range(self.n):
            mach += "1"

        a = self.mach2dec(mach)

        return a

    def smallest_number(self):
        f_sign = "1"
        man = ""
        for i in range(self.nm):
            man += "0"

        s_sign = "0"
        exp = ""
        for j in range(self.get_ne()):
            exp += "1"

        mach = f_sign + man + s_sign + exp
        ans = self.mach2dec(mach)

        return ans


class UI:
    def __init__(self):
        self.er = Machine.er
        self.suc = Machine.suc
        self.machine = Machine(1,1)
        self.init_machine()
        self.options = ["Get the biggest number of the Machine.",
                        "Get the smallest number of the Machine.",
                        "Get the epsilon of the machine.",
                        "Change a number in base 10 to a machine number.",
                        "Change a machine number to the equivalent number.",
                        "Change the current machine.",
                        "Quit"]
        self.options_dic = {1: (False, self.machine.biggest_number, False),
                            2: (False, self.machine.smallest_number, False),
                            3: (False, self.machine.epsilon, False),
                            4: (True, self.machine.dec2mach, False),
                            5: (True, self.machine.mach2dec, False),
                            6: (False, self.init_machine, True)}
        self.options_ask = ["",
                            "",
                            "",
                            "Write your number in base 10 (if it has a decimal part, use it as a point): ",
                            "Write your machine number: ",
                            ""]
        self.options_solve = ["The biggest number of your machine is: ",
                              "The smallest number of your machine is: ",
                              "The epsilon of your machine is: ",
                              "Your machine number is: ",
                              "Your equivalent number in base 10: "]

    def init_machine(self):
        while True:
            print(Colors.BOLD + "CREATE A MACHINE..." + Colors.END)
            while True:
                total = input("Write the number of total bits of the machine: ")
                if not re.fullmatch("[0-9]+", total) or int(total) <= 3:
                    print(Colors.FAIL + "Your input has to be a integer value bigger than 3.\n" + Colors.END)
                    print("\n")
                else:
                    break

            total = int(total)
            if total == 4:
                mantissa = 1
            else:
                repeat = False
                finish = False
                while True:
                    mantissa = input("Write the number of bits of the mantissa of the machine: ")
                    if not re.fullmatch("[0-9]+", mantissa):
                        print(Colors.FAIL + "Your input has to be a integer value.\n" + Colors.END)
                        print("\n")
                        continue

                    mantissa = int(mantissa)
                    if total <= mantissa + 2 or mantissa < 1:
                        print(Colors.FAIL + "The number of bits of the mantissa has to be at least 1 and "
                                            "at most " + str(total - 3) + "." + Colors.END)

                        while True:
                            rep = input("Do you want to change the bits of "
                                        "the machine previously written? [y/n]: ")

                            rep = rep.replace(" ", "")

                            regex_match = re.fullmatch("[ynYN]", rep)

                            if regex_match:
                                if rep == "y" or rep == "Y":
                                    repeat = True
                                break
                    else:
                        finish = True

                    if repeat or finish:
                        break

                if repeat:
                    print("\n")
                    continue

            break

        self.machine.set_machine(total, mantissa)
        if self.machine.get_ne() > 10:
            print(Colors.WARNING + "\nIt's possible that your computer is not able to handle the numbers that "
                                   "the created machine." + Colors.END)
            print("(press enter to accept)")
            input()
        return 0, Machine.suc

    def start(self):
        while True:
            inp, er = self.print_options()
            if er == self.suc:
                if inp == len(self.options):
                    print(Colors.BOLD + "\nThanks!" + Colors.END)
                    break

                inp -= 1
                execute = self.options_dic[inp + 1]
                if execute[0]:
                    num = input(self.options_ask[inp])
                    ans = execute[1](num)
                else:
                    ans = execute[1]()

                if ans[1] == self.suc and not execute[2]:
                    print("\n")
                    print(Colors.BLUE + self.options_solve[inp] + Colors.END + str(ans[0]))
                    print("This number will be saved in your clipboard for further use!")
                    pyperclip.copy(str(ans[0]))
                elif ans[1] == self.suc:
                    continue
                print("(press enter to continue)")
                input()

    def print_options(self):
        print(Colors.BOLD + "\n\n--------------------------" + Colors.END)
        print(Colors.HEADER + "You are using a machine with " + str(self.machine.n) + " bits, which has "
              + str(self.machine.nm) + " bits for the mantissa and " + str(self.machine.get_ne())
              + " bits for the exponent." + Colors.END)
        print("What do you want to do?")
        UI.print_array(self.options)

        len_opt = len(self.options)
        user_input = input(Colors.UNDERLINE + "\nWrite your pick!" + Colors.END + " ")
        user_input = user_input.replace(" ", "")

        if not re.fullmatch("[0-9]+", user_input):
            print(Colors.FAIL + "The input has to be an integer value" + Colors.END)
            return 0, self.er

        user_input = int(user_input)
        if user_input not in range(1, len_opt + 1):
            print(Colors.FAIL + "Not a valid pick, remember to use numbers from 1 to " +
                  str(len_opt) + "." + Colors.END)

            return 0, self.er

        print("\n")
        return user_input, self.suc

    @staticmethod
    def print_array(strings):
        i = 1
        for string in strings:
            print(Colors.BOLD + str(i) + ". " + Colors.END + string)
            i += 1


ui = UI()
ui.start()
