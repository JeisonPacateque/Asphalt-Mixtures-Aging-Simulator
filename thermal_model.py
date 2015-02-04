# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 00:01:43 2015

@author: santiago
"""

import numpy as np
import time
import laplacian

class ThermalModel(object):
    def __init__(self, matrix_materials, max_TC=7.8):
        """
        This class supports the thermal model thourgh difussion (laplacian)

        matrix_materials = initial matrix materials
        (numpy objetc array, array of class Material)

        maxTC = max transfer coefficient, important to define stability
        of dt in the model"""

        # reference of the matrix materials used only
        # to get transfer coeefficient amd  object construction
        self.MM  = matrix_materials.copy()

        #initial temperature field
        self.ui = np.zeros(self.MM.shape, dtype=np.float)
        self.u = self.ui.copy() # next step temperature field
        self.TCs = np.zeros(self.MM.shape, dtype=np.float)

#         copy all the thermal conductivities from the matrix materials
        for i in xrange(self.MM.shape[0]):
                for j in xrange(self.MM.shape[1]):
                    self.TCs[i,j] = self.MM[i,j].thermal_conductivity

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
        self.dt = self.dx2*self.dy2/(max_TC**(self.dx2 + self.dy2))
        print "dt = ", self.dt

    def applySimulationConditions(self, ambient=40, internal=10):
        """"Set the temperatures for the simulation"""

        self.ui.fill(internal)    # internal temperature in asphalt
        self.ui[:10,:] = ambient # applied temperature from environment

        print "Applied internal temperature in the asphalt:", internal
        print "applied temperature from environment:", ambient

    def simulate(self, n_steps=10000):
        """"This function executes the model in number steps (n_steps)"""

        steps = np.arange(n_steps)
        start_time = time.time()  # Measures file loading time

        for step in np.nditer(steps):
            print "Thermal simulation step:", step
            self. u = laplacian.evolve_ts(self.ui, self.u, self.TCs,
                                self.dt, self.dx2, self.dy2)
            self.ui = self.u.copy()

        # copy the field temperature into the matrix materials
        for i in xrange(self.MM.shape[0]):
            for j in xrange(self.MM.shape[1]):
                self.MM[i,j].temperature = self.u[i,j]

        end_time = time.time()  # Get the time when method ends
        print "Thermal simulation done in ", str(end_time - start_time), " seconds."
        return self.MM