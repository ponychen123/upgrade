#!/usr/bin/python3
##########################################################################
#                        MEPSearcher (V2.0_alpha)                        #   
#  1. Brief Introducation                                                #
#     A program searching Minimum Energy Paths(MEP).                     #
#     Current version is based on "string method" which is develeped     #
#     by Weinan E et al. [ Phys.Rev.B 66, 052301(2002)]                  #
#  2. Technical details                                                  #
#     3 modules are used in this program                                 #
#       -io: input and output                                            #
#       -optmize: optimize beads                                         #
#       -redistribute: redistribute beads along MEPS                     #
#     Alglib is used to do interpolation, so at least you should         #
#     install this math module                                           #
#     draw.py is used to quickly visiualize results, some additional     #
#     modules are needed                                                 #
#  3. history                                                            #
#     2016.02.18                                                         #
#     Dr Chen Xin first release version v1.0_alpha with python2 on github#
#     2019.04.11                                                         #
#     pony chen rewrite and tidy all the codes with python3, added cg    #
#     converge method and write draw.py script, forther NEB function     #
#     will be added                                                      #
#           Developer:  pony chen                                        #
#               Email: cjchen16s@imr.ac.cn                               #
#                                               2019.04.11               #
##########################################################################
from iio import *
from optimize import *
from redistribute import *
import xalglib

##### SETTINGS ######
Max_iter = 100000     #maximum iretation steps
Tol = 1e-5          #converge tolerance
h = 0.05          #step size, 0.5 is okay for most case
o = 'sd'            #'cg' or 'sd'
####################

FILE_PES = open("PES.data", "r")
FILE_Iniguess = open("guess.data", "r")
FILEOUT = open("out.data", "w")

# read PES(potential energy surface)
X_PES, Y_PES, E_PES = PESreadin(FILE_PES)

# read initial guess path
string0 = Iniguessreadin(FILE_Iniguess)

# Searching the MEP on PES 
N_iter = 0
while N_iter < Max_iter:
    N_iter += 1

    #### update beads ####
    if o == 'cg':
        string = optmizestringcg(X_PES, Y_PES, E_PES, string0, h)
    elif o == 'sd':
        string = optmizestringsd(X_PES, Y_PES, E_PES, string0, h)
    else:
        print("please set o to tell me which mode to converge")
        break
    string = redistribute(string)
    
    ### check the convergency ###
    ds = 0
    for i in range(len(string)):
        dx = (string[i][0] - string0[i][0])**2
        dy = (string[i][0] - string0[i][0])**2
        ds += (dx + dy)**0.5

    if ds < Tol:
        print("Successful !")
        break
    
    #OUTPUT every 30 steps
    if N_iter % 30 == 0:
        print("STEP: ", N_iter, ";   diff  = ", ds)

    string0 = string

#output all the results
print("Final steps = ", N_iter)
printresult(FILEOUT, string, X_PES, Y_PES, E_PES)
