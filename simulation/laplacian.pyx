'''
Copyright (C) 2015 Jeison Pacateque, Santiago Puerto

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
'''

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