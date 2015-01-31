# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 00:01:43 2015

@author: santiago
"""

import numpy as np

class ThermalModel(object):
    def __init__(self, matrix_materials, max_TC=7.8):
        """MM_i = initial matrix materials
        (numpy objetc array, array of class Material)
        maxTC = max transfer coefficient, important to define stability
        of dt in the model"""

        self.MM_i = np.empty(matrix_materials.shape, dtype=float)

        # copy all the temperature values in the matrix materials
        for i in range(self.MM_i.shape[0]):
                for j in range(self.MM_i.shape[1]):
                    self.MM_i[i,j] = matrix_materials[i,j].temperature

        self.MM = self.MM_i.copy() #next step matrix

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

        for i in range(self.MM_i.shape[0]):
            for j in range(self.MM_i.shape[1]):
                self.MM_i[i, j].temperature = ambient

        for i in range(4):
            for j in range(3):
                self.MM_i[i, j].temperature = applied

        print "Applied temperature over asphalt mixture:", applied
        print "Ambient temperature:", ambient

    def _getThermalConductivity(self, i, j):
        """Obtain the thermal conducitvity from element i,j"""
        return self.MM[i,j].thermal_conductivity

    def _evolve_ts(self):
        """
        This function evaluate the derivatives in the Laplacian, and
        calculates MM[i,j] based on MM_i[i,j].
        """

        for i in range(self.MM_i.shape[0]-1):
            for j in range(self.MM_i.shape[1]-1):
                uxx = (self.MM_i[i+1,j].temperature -
                2*self.MM_i[i,j].temperature +
                self.MM_i[i-1,j].temperature)/self.dx2

                uyy = (self.MM_i[i,j+1].temperature -
                2*self.MM_i[i,j].temperature +
                self.MM_i[i,j-1].temperature)/self.dy2

                TC = self._getThermalConductivity(i,j)

                self.MM[i,j].temperature = self.MM_i[i,j].temperature
                + self.dt*float(TC)*(uxx+uyy)

    def simulate(self, n_steps=500):
        """"This function executes the model in number steps (n_steps)"""
        steps = np.arange(n_steps)
        for step in np.nditer(steps):
            self._evolve_ts()
            for i in range(self.MM_i.shape[0]):
                for j in range(self.MM_i.shape[1]):
                    self.MM_i[i, j].temperature = self.MM[i, j].temperature
            print step