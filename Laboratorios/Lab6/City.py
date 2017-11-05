from DataStructures import DigraphAL

class City:
    def readFile():
        f1 = open('medellin.txt','r') #Format -> ID  CoordX  CoordY  Name
        IDs = []
        n = [i for i in range(310153)]
        for line in f:
            lineL = line.split(' ')
            IDs.append(lineL[0])
        IDs_Index = dict(zip(IDs,n))
        G = DigraphAL(310153)
        f2 = open('connection.rtf','r') #Format -> ID ID distancia nombre
City.readFile()
