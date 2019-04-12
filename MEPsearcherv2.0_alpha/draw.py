#!/usr/bin/python3
#this scripts was written to quickly draw the calculated MEP
#you should change the variable levels to match your results
#this scripts is writen by pony chen at 2019/4/10

import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata as gd

MIN, MAX, STEP = -1.0, 1.3 , 0.1   #the enrgy level min max value 
FILE_PES = open("PES.data","r")    #and step size of energy range
FILE_MEP = open("out.data","r")
FILE_Ini = open("guess.data","r")

def PESreadin(FILE):
    #read the PESdata and split it 
    lines = FILE.readlines()
    X = []
    Y = []
    E = []
    XY = []
    for line in lines:
        line_split = line.split()
        X.append(float(line_split[0]))
        Y.append(float(line_split[1]))
        E.append(float(line_split[2]))
        XY.append([float(line_split[0]),float(line_split[1])])

    return X, Y, E, XY
def MEPreadin(FILE):
    #read the out.data and split it
    lines = FILE.readlines()
    X = []
    Y = []
    for line in lines:
        line_split = line.split()
        X.append(float(line_split[0]))
        Y.append(float(line_split[1]))
    return X, Y
def Inireadin(FILE):
    #read the initial guess path
    lines = FILE.readlines()
    Nbeads = int(lines[0])
    firstcoors = lines[1].split()
    lastcoors = lines[2].split()
    firstcoor = [float(firstcoors[0]), float(firstcoors[1])]
    lastcoor = [float(lastcoors[0]), float(lastcoors[1])]
    X = []
    Y = []
    delta_X = (lastcoor[0] - firstcoor[0])/(Nbeads-1)
    delta_Y = (lastcoor[1] - firstcoor[1])/(Nbeads-1)
    for i in range(Nbeads):
        X.append(i*delta_X+firstcoor[0])
        Y.append(i*delta_Y+firstcoor[1])
    return X, Y

X_PES, Y_PES, E_PES, XY_PES = PESreadin(FILE_PES)
points = np.array(XY_PES)
E = np.array(E_PES)
X1 = np.array(X_PES)
Y1 = np.array(Y_PES)

#intepolate X_PES and Y_PES to get X-Y meshgrid
X1 = np.linspace(X1.min(), X1.max(), 1000)
Y1 = np.linspace(Y1.min(), Y1.max(), 1000)
X1, Y1 = np.meshgrid(X1, Y1)

#intepolate Z over X-Y meshgrid above
Z = gd(points, E, (X1, Y1), method='cubic')

X_MEP, Y_MEP = MEPreadin(FILE_MEP)
X_ini, Y_ini = Inireadin(FILE_Ini)


#draw the PES and MEP and initial guess path
levels = np.arange(MIN, MAX, STEP)
fig, ax = plt.subplots(figsize=(5,5))
CS = ax.contour(X1, Y1, Z, levels, colors='k',
        linewidths=1, extent=(-1.5,1.5,-1.5,1.5))
ax.contourf(X1,Y1,Z,levels, cmap=plt.cm.jet)
ax.clabel(CS, levels[::2],inline=1, fontsize=10)
ax.set_title('finally gained MEP')
ax.scatter(X_MEP, Y_MEP, s=30, c='black')
ax.scatter(X_ini, Y_ini, s=30, c='r')
plt.show()
