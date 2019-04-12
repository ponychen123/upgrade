import matplotlib.pyplot as plt
import numpy as np

FILE = open("PES.data", "w")
def f(x, y):
    return np.sin(x)**10+np.cos(10+y*x)*np.cos(x)

x = np.linspace(0, 6, 100)
y = np.linspace(0, 6, 100)

X, Y = np.meshgrid(x, y)

Z = f(X, Y)
X = X.reshape(-1, 1)
Y = Y.reshape(-1, 1)
E = Z.reshape(-1, 1)

#print(X)
print(Z.min(), Z.max())

for i in range(len(X)):
    string = str(X[i][0]) + "    " + str(Y[i][0]) + "    " + str(E[i][0]) + "\n"
    FILE.write(string)
