# -*- coding: utf-8 -*-
"""
Created on Wed Feb  4 11:54:15 2015

@author: sjdps
"""

cimport numpy as np
import numpy as np
import cython

@cython.boundscheck(False) # turn of bounds-checking for entire function
def evolve_ts(np.ndarray[np.float64_t, ndim=2] ui,
              np.ndarray[np.float64_t, ndim =2] u, \
              np.ndarray[np.float64_t, ndim=2] TCs, \
              double dt, double dx2, double dy2):

        cdef unsigned i, j

        for i in xrange(1, u.shape[0]-1):
            for j in xrange(1, u.shape[1]-1):
                uxx = (ui[i+1,j] - 2*ui[i,j] + ui[i-1, j] )/dx2
                uyy = (ui[i,j+1] - 2*ui[i,j] + ui[i, j-1] )/dy2
                TC = TCs[i,j]
                u[i,j] = ui[i,j] + dt*TC*(uxx+uyy)

        return u