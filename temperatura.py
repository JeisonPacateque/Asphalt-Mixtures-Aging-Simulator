# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 21:59:54 2014

@author: sjdps
"""

#jacobi2d temperatura
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib import cm

n = 120
tol = 0.1 / (n+1)**2
maxiter = 100000

clock_start, clock_finish, clock_rate=0, 0, 0

h = 1.0/n
#print h
archivo=open("solutions.txt", "w")

X = np.arange(0, 1, h)
Y = np.arange(0, 1, h)

U = np.zeros((n,n))
F = np.zeros((n,n))

#U[:,0]=0
#U[0,:]=0


for i in xrange(n):
    if X[i] <= 0.3 or X[i]>= 0.7:
        U[i, n-1]=0    
    else:        
        U[i, n-1]=1
    
    if Y[i] <= 0.3 or Y[i] >= 0.7:
        U[n-1, i] = 0
    else:
        U[n-1, i] = 1

for it in xrange(1,200):
    Uold = U
    dumax = 0
    
    print it
    for j in xrange(n-1):
        for i in xrange(n-1):
            U[i,j]=0.25*(Uold[i-1,j] + Uold[i+1,j] + Uold[i,j-1] + Uold[i,j+1] + (h**2)*(F[i,j]))
#            U[i,j]=0.25*(Uold[i-1,j] + Uold[i+1,j] + Uold[i,j-1] + Uold[i,j+1])
            dumax=max(dumax, abs(U[i,j]-Uold[i,j]))
    

plt.figure(1)                  
plt.clf()                      # clear figure
plt.pcolor(X,Y,U,cmap=cm.jet)  # pseudo-color plot using colormap "jet"
plt.axis('scaled') 

plt.clim(0., 1.)               # colors range from u=0 to u=1
plt.colorbar()                 # add a color bar to show temperature scale
plt.title('Temperature')
plt.show()


plt.figure(2)                  
plt.clf()                     
            
# contour line levels:
clines = np.linspace(0., 1., 26)

# do contour plot:
C = plt.contour(X,Y,U,clines,colors='k') 
plt.axis('scaled')             # so x- and y-axis scaled the same (square)

# add labels on every other line:
plt.clabel(C, clines[1::2], inline=1, fontsize=10)

plt.title('Contours of temperature')

#plt.savefig('contour.png')
plt.show()