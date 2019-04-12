import xalglib

#steepest descent or conjugate gradient optimization is
#used in this module
#2019.04.11 pony chen

def optmizestringsd(X, Y, E, S, h):
    #the string is optimized by sd method
    S_new = []
    inter = xalglib.spline2dbuildbicubicv(X, len(X), Y, len(Y), E, 1)
    for coor in S:
        Ener, dx, dy, dxy = xalglib.spline2ddiff(inter, coor[0], coor[1])
        S_new.append([coor[0]-h*dx, coor[1]-h*dy])
    return S_new

def optmizestringcg(X, Y, E, S, h):
    #the string is optimized by cg method
    S1, S_new = [], []
    n = len(S)
    dx = list(range(n))
    dy = list(range(n))

    inter = xalglib.spline2dbuildbicubicv(X, len(X), Y, len(Y), E, 1)
    
    #steep descent step
    for i in range(n):
        Ener, dx[i], dy[i], dxy = xalglib.spline2ddiff(inter, S[i][0], S[i][1])
        S1.append([S[i][0]-h*dx[i], S[i][1]-h*dy[i]])
    
    #orthogonal step
    for i in range(n):
        Ener, Dx, Dy, Dxy = xalglib.spline2ddiff(inter, S1[i][0], S1[i][1])
        a = Dx*dx[i] + Dy*dy[i]
        b = dx[i]**2 + dy[i]**2
        lamda = a/b
        D1x = Dx - lamda*dx[i]
        D1y = Dy - lamda*dy[i]
        S_new.append([S1[i][0]-h*D1x, S1[i][1]-h*D1y])

    return S_new
    
