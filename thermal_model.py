# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 00:01:43 2015

@author: santiago
"""

#import matplotlib.pyplot as plt
import numpy as np

class ThermalModel(object):
    def __init__(self, MM_i, max_TC=7.8):
#        MM_i.transpose()
        self.MM_i = MM_i
        self.MM = self.MM_i.copy() #ciudado con esta operacion

        print type(MM_i)
        print MM_i[0,0].temperature
        MM_i[0,0].temperature = 41456465

        # Calculate dx, dy
        self.lengthX = self.MM_i.shape[0]
        self.lengthY = self.MM_i.shape[1]
        dx = 1./self.lengthX
        dy = 1./self.lengthY
        self.dx2 = dx**2 # To save CPU cycles, we'll compute Delta x^2
        self.dy2 = dy**2 # and Delta y^2 only once and store them.
        print "dx2=", self.dx2
        print "dy2=", self.dy2

        # For stability, this is the largest interval possible
        # for the size of the time-step:
        self.dt = self.dx2*self.dy2/(float(max_TC)*(self.dx2 + self.dy2))

    def applySimulationConditions(self, ambient=20, applied=100):
        """"Set the temperatures for the simulation """
        print self.MM_i.shape
#        for (i,j), _ in np.nditer(self.MM_i, flags=['refs_ok']):
#            self.MM_i[i, j].material = ambient

        for i in range(self.MM_i.shape[0]):
            for j in range(self.MM_i.shape[1]):
                self.MM_i[i, j].material = ambient

        for i in range(4):
            for j in range(3):
                self.MM_i[i, j].material = applied

        print "Applied temperature over asphalt mixture:", applied
        print "Ambient temperature:", ambient

    def _getThermalConductivity(self, i, j):
        """Obtain the thermal conducitvity from element i,j"""
        return self.MM[i,j].thermal_conductivity

    def _evolve_ts(self):
        """
        This function uses two plain Python loops to
        evaluate the derivatives in the Laplacian, and
        calculates u[i,j] based on ui[i,j].
        """
#        for (i,j), _ in np.nditer(self.MM_i, flags=['refs_ok']):
        for i in range(self.MM_i.shape[0]-1):
            for j in range(self.MM_i.shape[1]-1):
                uxx = (self.MM_i[i+1,j].temperature -
                2*self.MM_i[i,j].temperature +
                self.MM_i[i-1,j].material)/self.dx2

                uyy = (self.MM_i[i,j+1].material -
                2*self.MM_i[i,j].material +
                self.MM_i[i,j-1].material)/self.dy2

                TC = self._getThermalConductivity(i,j)

                self.MM[i,j].material = self.MM_i[i,j].material
                + self.dt*float(TC)*(uxx+uyy)

    def simulate(self, steps=500):
        """"Show the evolution of the thermical simulation"""
        a = np.arange(steps)
        for x in np.nditer(a):
            self._evolve_ts()
            for i in range(self.MM_i.shape[0]-1):
                for j in range(self.MM_i.shape[1]-1):
                    self.MM_i[i, j].material = self.MM[i, j].material


        print "Done!"