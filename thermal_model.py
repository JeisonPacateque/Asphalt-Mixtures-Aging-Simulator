# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 00:01:43 2015

@author: santiago
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

class ThermalModel(object):
    def __init__(self, matrix_materials, max_TC=7.8):
        """initial matrix materials
        (numpy objetc array, array of class Material)
        maxTC = max transfer coefficient, important to define stability
        of dt in the model"""

        # reference of the matrix materials used only
        # to get transfer coeefficient amd  object construction
        self.MM  = matrix_materials

        #initial temperature field
        self.ui = np.zeros(matrix_materials.shape)

        # copy all the temperature values from the matrix materials
        for i in range(self.MM.shape[0]):
                for j in range(self.MM.shape[1]):
                    self.ui[i,j] = self.MM[i,j].temperature

        self.u = self.ui.copy() # next step temperature field

        # Calculate dx, dy
        self.lengthX = self.MM.shape[0]
        self.lengthY = self.MM.shape[1]
        dx = 1./self.lengthX
        dy = 1./self.lengthY
        self.dx2 = dx**2 # To save CPU cycles, we'll compute Delta x^2
        self.dy2 = dy**2 # and Delta y^2 only once and store them.
        print "dx2=", self.dx2
        print "dy2=", self.dy2

        # For stability, this is the largest interval possible
        # for the size of the time-step:
        self.dt = self.dx2*self.dy2/(float(max_TC)*(self.dx2 + self.dy2))
        print "dt = ", self.dt

    def applySimulationConditions(self, ambient=40, internal=10):
        """"Set the temperatures for the simulation"""

        self.ui.fill(internal)    # internal temeperature in asphalt
        self.ui[-10:,:] = ambient # applied temperature from environment

        print "Applied internal temperature in the asphalt:", internal
        print "applied temperature from environment:", ambient

    def _getThermalConductivity(self, i, j):
        """Obtain the thermal conducitvity from element i,j
        private method"""

        return float(self.MM[i,j].thermal_conductivity)

    def _evolve_ts(self):
        """
        This function evaluate the derivatives in the Laplacian, and
        calculates u[i,j] based on ui[i,j]. Private method
        """
#        for (i,j), _ in np.ndenumerate(self.u[:-1, :-1]):
        for i in xrange(1, self.lengthX-1):
            for j in xrange(1, self.lengthY-1):
                uxx = ( self.ui[i+1,j] - 2*self.ui[i,j] + self.ui[i-1, j] )/self.dx2
                uyy = ( self.ui[i,j+1] - 2*self.ui[i,j] + self.ui[i, j-1] )/self.dy2
#                TC = self._getThermalConductivity(i,j)
                self.u[i,j] = self.ui[i,j]+self.dt*0.75*(uxx+uyy)

    def simulate(self, n_steps=100):
        """"This function executes the model in number steps (n_steps)"""

        steps = np.arange(n_steps)
        for step in np.nditer(steps):
            self._evolve_ts() # Laplacian cicle
            self.ui = self.u.copy()
            print step

#        salida =self.ui.copy()
#
#        plt.imshow(salida)
##        plt.imshow(salida, cmap=cm.jet, interpolation='nearest', origin='lower')
#        plt.colorbar()
#        plt.show()
#        np.set_printoptions(threshold=np.inf, linewidth=np.inf)
#        with open('mapa_termico.txt', 'w') as f:
#            f.write(np.array2string(salida, separator=', '))

        # copy the field temperature into the matrix materials
        for i in range(self.MM.shape[0]):
            for j in range(self.MM.shape[1]):
                self.MM[i,j].temperature = self.u[i,j]



#        heatmap = np.zeros(self.MM.shape)
#
#        for i in range(self.MM.shape[0]):
#            for j in range(self.MM.shape[1]):
#                heatmap[i,j] = self.MM[i,j].temperature

        plt.imshow(self.u)
#        plt.imshow(heatmap, cmap=cm.jet, interpolation='nearest', origin='lower')
#        plt.axis([heatmap.min(), heatmap.max(), heatmap.min(), heatmap.max()])
        plt.colorbar()
        plt.show()

        return self.MM
