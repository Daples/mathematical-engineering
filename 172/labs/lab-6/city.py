from data-strucutres import DigraphAL

class City:
    class nodeObj:
        def __init__(self, ID, x, y, name):
            self.ID = ID
            self.x = x
            self.y = y
            self.name = name

    def readFile():
        f1 = open('medellin.txt','r') #Format -> ID  CoordX  CoordY  Name
        IDs = []
        n = [i for i in range(310153)]
        nodes = [] #Info
        for line in f1:
            lineL1 = line.split(' ')
            nodes.append(City.nodeObj(lineL1[0],float(lineL1[1]),float(lineL1[2]),lineL1[3]))
            IDs.append(float(lineL1[0]))
        IDs_Index = dict(zip(IDs,n))

        G = DigraphAL(310153) #Initialize the graph
        f2 = open('connection.rtf','r') #Format -> ID ID distancia nombre
        for line in f2:
            lineL2 = line.split(' ')
            G.insert(IDs_Index[float(lineL2[0])], IDs_Index[float(lineL2[1])], float(lineL2[2]), Name=lineL2[3])
City.readFile()
