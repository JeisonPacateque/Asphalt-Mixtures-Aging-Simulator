# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 21:59:54 2014

@author: sjdps
"""


#jacobi2d temperatura
cimport numpy as np
import numpy as np
import cython

@cython.boundscheck(False)
def difusion(unsigned int maxiter, unsigned int n):
    cdef unsigned int i, j, it1, it2
    cdef double tol = 0.1 / (n+1)**2
    cdef double dumax

    #clock_start, clock_finish, clock_rate=0, 0, 0

    cdef double h = 1.0/n

    cdef np.ndarray[double, ndim=1] X = np.arange(0, 1, h)
    #Y = np.arange(0, 1, h)
    cdef np.ndarray[double, ndim=1] Y = np.arange(0, 1, h)

    #U = np.zeros((n,n))
    cdef np.ndarray[double, ndim=2] U = np.zeros((n, n))

    cdef np.ndarray[double, ndim=2] Uold = np.zeros((n, n))
    #F = np.zeros((n,n))
    cdef np.ndarray[double, ndim=2] F = np.zeros((n, n))

    U[:,-1] = 1   #Calor en la tapa de arriba
    
#    for it1 in xrange(n):
#        if X[it1] <= 0.3 or X[it1]>= 0.7:
#            U[it1, n-1]=0
#        else:
#            U[it1, n-1]=1
    U[-1, :] = 1 #Calor en la tapa de la derecha

#        if Y[it1] <= 0.3 or Y[it1] >= 0.7:
#            U[n-1, it1] = 0
#        else:
#            U[n-1, it1] = 1


    for it2 in xrange(maxiter):
        for i in xrange(n):
            for j in xrange(n):
                Uold[i, j] = U[i, j]

        dumax = 0

        for j in xrange(1,n-1):
            for i in xrange(1,n-1):
#                U[i,j]=0.25*(Uold[i-1,j] + Uold[i+1,j] + Uold[i,j-1] + Uold[i,j+1] + (h**2)*(F[i,j]))
#                U[i,j] = 0.25*(Uold[i-1,j] + Uold[i+1,j]\
#                                + Uold[i,j-1] + Uold[i,j+1])
                U[i, j] = 0.25*( Uold[<unsigned int>(i-1), j] +\
                                Uold[i+1,j] + Uold[i, j+1] + \
                                Uold[i, <unsigned int>(j-1)])
                dumax = max(dumax, abs(U[i,j]-Uold[i,j]))

    return X, Y, U