import random
import string
import time
from data-structures import LinkedList

def random_string(N):
	return ''.join(random.choices('abcd[ef]ghi', k=N))

def manage_string(string):
    ll = LinkedList()
    array = string.split("\n")
    resp = ""
    for line in array:
        ll.clear()
        index = 0
        for char in line:
            if char == "[":
                index = 0
            elif char == "]":
                index = ll.size()
            else:
                ll.insert(char, index)
                index += 1

        for item in ll:
            resp += item
        resp += "\n"

    return resp

def timeString():
    file = open('Time.csv','w+')
    for i in range(2,7):
        s = random_string(10**i)
        now = time.clock()
        manage_string(s)
        after = time.clock()
        delta = after - now
        file.write(str(delta) + ',')
timeString()
