import random
import time
import sys
import subprocess
import numbers
import matplotlib.pyplot as pt
import numpy


sys.setrecursionlimit(100000)
nameOfFile = 'Tables.csv'
myFile = open(nameOfFile, 'w')
names = ('ArraySum: \n', 'ArrayMax: \n', 'Fibonacci: \n')


def arraysum(nums, i):
	"""
	:param nums: arrary with numbers
	:param i: index in the array
	:return: the sum of all the numbers of the array
	"""
	if (i == 0):
		return nums[0]
	return nums[i] + arraysum(nums,i-1)

def arraymax(nums,n):
	"""
	:param nums: arrary with numbers
	:param n: index in the array
	:return: the biggest number of the array
	"""
	max = nums[n]
	if (n != 0):
		temp = arraymax(nums, n-1)
		if (temp > max):
			max = temp
	return max
	
def fibonacci(n):
	"""
	:param n: the wanted fibonacci number
	:return: the nth fibonacci number
	"""
	if (n<=1):
		return n
	return fibonacci(n-1) + fibonacci(n-2)

def randomarray(n):
	"""
	:param n: the size of the array
	:return: a random array with size n
	"""
	return [random.random() for e in range(n)]
	
def printinfile(methodToRun, *args):
	"""
	Prints the time to run in a file
	:param methodToRun: the method that you're going to test
	:param args: the arguments that the method needs
	:return: nothing
	"""
	now = time.clock()*1000000000
	methodToRun(*args)
	after = time.clock()*1000000000
	myFile.write('\n'+str(after - now))

def uploadgit(direction, comment, *args):
	"""
	Uploads files to git
	:param direction: the direction of the git to upload
	:param comment: the comment of the upload
	:param args: the files to upload
	:return: nothing
	"""
	subprocess.call(["cd", "~/" + direction])
	for arg in args:
		subprocess.call(["git add", arg])
		subprocess.call(["git commit", comment])
		subprocess.call(["git push", ""])
		
def timesinmethods():
	"""
	Calculates the time of each method
	:return: nothing
	"""
	myFile.write('ArrayMax: ')
	for i in range(1,5):
		printinfile(arraysum, randomarray(10**i), 10**i-1)

	myFile.write('\nArraySum: ')
	for i in range(1,5):
		printinfile(arraymax, randomarray(10**i), 10**i-1)

	myFile.write('\nFibonacci: ')
	for i in range(4,17,4):
		printinfile(fibonacci, i)
	myFile.close()
		

timesinmethods()



