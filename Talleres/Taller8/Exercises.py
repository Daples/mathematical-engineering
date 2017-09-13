from DataStruct import Stack
from collections import deque
import re

def backwards(*args):
	myStack = Stack(len(args))
	for item in args:
		myStack.push(item)

	backStack = Stack(len(args))
	for i in range(len(args)):
		backStack.push(myStack.pop())

	return backStack

def racistQueue(*args):
	j = len(args)-1
	queue = deque([])
	while j >= 0:
		queue.append(args[j])
		j -= 1

	for i in range(len(args)):
		print("Attending:", queue.pop())

def polacNotation(equation):
	equation = re.sub('[" "a-zA-Z,.:;]', "", equation)
	stack = Stack(len(equation))
	for num in equation:
		stack.push(num)

	while len(stack.data) > 1:
		op1 = stack.pop()
		op2 = stack.pop()
		op3 = stack.pop()
		result = eval(op2+op3+op1)
		stack.push(str(result))

	return stack.pop()
