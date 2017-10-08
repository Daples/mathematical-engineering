from DataStructures import LinkedList, Queue

class Bank:

    def __init__(self):
        self.lines = LinkedList()
        self.cashiers = LinkedList()
        self.cashiers.insert(2)
        self.cashiers.insert(1)
        self.total = 0

    def aux_line(self, names):
        queue = Queue()
        for i in names:
            queue.push(i)
        self.lines.insert(queue)
        self.total += len(names)

    def line(self, names):
        i = len(names) - 1
        while i >= 0:
            self.aux_line(names[i])
            i -= 1

    def simulation(self):
        mv_line = self.lines.first
        mv_cashier = self.cashiers.first
        cAux = 0
        count = 0
        while True:
            if count == self.total:
                break
            if cAux == 4:
                mv_line = self.lines.first
                cAux = 0
            if mv_line.node.ll.int_size != 0:
                print(str(mv_line.node.pop()) + ' was attended by cashier ' + str(mv_cashier))
            else:
                mv_line = mv_line.next
                cAux += 1
                continue
            count += 1
            mv_line = mv_line.next
            if mv_cashier.next is not None:
                mv_cashier = mv_cashier.next
            else:
                mv_cashier = self.cashiers.first
            cAux += 1

    def printLines(self):
        count = 1
        for i in self.lines:
            print('Line {} {}'.format(count,i))
            count += 1


if __name__ == '__main__':
    a = Bank()
    a.line([['Lola', 'Manola'], ['Frodo','Maggi'],['Sergio'],['Frederic','Adolf','Ivan','Joseph']])
    a.printLines()
    a.simulation()
