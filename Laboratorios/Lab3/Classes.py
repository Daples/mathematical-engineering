class Fridge:

    def __init__(self, num, desc):
        self.num = num
        self.desc = desc

    def __str__(self):
        return "(" + str(self.num) + ", " + self.desc + ")"


class Order:

    def __init__(self, name, num):
        self.name = name
        self.num = num

    def __str__(self):
        return "(" + self.name + ", " + str(self.num) + ")"