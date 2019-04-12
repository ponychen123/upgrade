import xalglib

def redistribute(S):
    #equal redistribute all beads on the string
    n = len(S)
    
    #calculate DS as an reference for the distribution of beads
    ds = list(range(n))
    ds[0] = 0
    for i in range(1, n):
        ds[i] = ((S[i][0] - S[i-1][0])**2 + 
                (S[i][1] - S[i-1][1])**2)**0.5

    Sum = 0
    tol = sum(ds)
    DS = list(range(n))
    for i in range(n):
        Sum += ds[i]
        DS[i] = Sum/tol
    
    #create an arithmetic progression standing for uniformly distributed beads.
    h = [ x/(n-1) for x in range(n)]

    #split the old string
    x, y = [], []
    for i in range(n):
        x.append(S[i][0])
        y.append(S[i][1])

    #interpolation
    interx = xalglib.spline1dbuildcubic(DS, x)
    intery = xalglib.spline1dbuildcubic(DS, y)

    S_new = []
    for i in range(n):
        x_new = xalglib.spline1dcalc(interx, h[i])
        y_new = xalglib.spline1dcalc(intery, h[i])
        S_new.append([x_new, y_new])
    return S_new

    

