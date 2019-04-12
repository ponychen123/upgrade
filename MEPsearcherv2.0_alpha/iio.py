import xalglib

#input and output data
#amazingly, i wanna to set the name 'io.py', but error happening in python3
#once i run it. thus i rename this module 'iio.py'...........

def PESreadin(FILE):
    #readin the PES.data and split it
    lines = FILE.readlines()
    PES_data, X, Y, E, Xf, Yf = [], [], [], [], [], []
    
    for line in lines:
        line_split = line.split()
        PES_data.append(line_split)
        
        #don't using set() function because it return dictrionay {}
        if line_split[0] not in X:
            X.append(line_split[0])
        if line_split[1] not in Y:
            Y.append(line_split[1])
    
    #the x loop must lie in the y loop, because the spline2dbuildcubicv 
    #function read the data at a specific oder
    for y in Y:
        for x in X:
            for line in PES_data:
                if x == line[0] and y == line[1]:
                    E.append(float(line[2]))
                    break
    Xf = [float(x) for x in X]
    Yf = [float(y) for y in Y]
                
    return Xf, Yf, E
    
def Iniguessreadin(FILE):
    #readin the initial path data
    lines = FILE.readlines()
    nbeads = int(lines[0])
    firstcoors = lines[1].split()
    lastcoors = lines[2].split()
    firstcoor = [float(firstcoors[0]), float(firstcoors[1])]
    lastcoor = [float(lastcoors[0]), float(lastcoors[1])]
    delta_x = (lastcoor[0] - firstcoor[0])/(nbeads - 1)
    delta_y = (lastcoor[1] - firstcoor[1])/(nbeads - 1)
    string = []
    for i in range(nbeads):
        tmp = [i * delta_x + firstcoor[0], i * delta_y + firstcoor[1]]
        string.append(tmp)
    return string

def printresult(FILE, S, X, Y, E):
    #print all the relative results
    inter = xalglib.spline2dbuildbicubicv(X, len(X), Y, len(Y), E, 1)
    for coor in S:
        E_new = xalglib.spline2dcalcv(inter, coor[0], coor[1])
        string = str(coor[0]) + "    " + str(coor[1]) + "    " + str(
                E_new[0]) + "\n"
        FILE.write(string)

