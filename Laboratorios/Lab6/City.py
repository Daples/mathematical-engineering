#from DataStructure import Graph
class City:
    def readFile():
        G = Graph()
        f = open('test.txt','r') #Format -> ID  CoordX  CoordY  Name
        for line in f:
            lineL = line.split(' ')
            
