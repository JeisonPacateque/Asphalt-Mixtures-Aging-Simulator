# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 00:01:43 2015

@author: santiago
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from PyQt4 import QtGui, QtCore
from pylab import cm


class ThermalModel(QtGui.QDialog):
    def __init__(self, materials, parent=None):
        super(ThermalModel, self).__init__(parent)
               
        
        self.ui = np.zeros((materials.shape)) # matriz inicial de temp
        self.u = np.zeros((materials.shape)) # matriz inicial de temp
        self.applySimulationConditions() 
        
                  #Calculate dx, dy
        self.dx = 1./materials.shape[0]
        self.dy = 1./materials.shape[1]
        self.dx2=self.dx**2 # To save CPU cycles, we'll compute Delta x^2
        self.dy2=self.dy**2 # and Delta y^2 only once and store them.
        print "dx2=", self.dx2
        print "dy2=", self.dy2
        # For stability, this is the largest interval possible
        # for the size of the time-step:
        self.dt = self.dx2*self.dy2/(7.8**(self.dx2+self.dy2) )

    def applySimulationConditions(self, ambient=20, applied=100):
        """"Set the temperatures for the simulation """
        self.ui.fill(ambient)    #temperatura ambiente
        self.ui[-10:, :] = applied #temperatura aplicada
        print "Applied temperature over asphalt:", applied
        print "Ambient temperature:", ambient

    def get_a(self, i, j):
        """Method to get an specific index of the thermal coeficients"""
        return 0.75

    def evolve_ts(self, u, ui):
        """
        This function uses two plain Python loops to
        evaluate the derivatives in the Laplacian, and
        calculates u[i,j] based on ui[i,j].
        """
        for i in range(1,u.shape[0]-1):
            for j in range(1,u.shape[1]-1):
                uxx = ( ui[i+1,j] - 2*ui[i,j] + ui[i-1, j] )/self.dx2
                uyy = ( ui[i,j+1] - 2*ui[i,j] + ui[i, j-1] )/self.dy2
                a = self.get_a(i, j)
                u[i,j] = ui[i,j]+self.dt*a*(uxx+uyy)
        return ui

    def simulate(self, steps=500):
        """"Show the evolution of the thermical simulation"""
        for x in range(0, steps):
            self.ui = self.evolve_ts(self.u, self.ui)
    
            self.ui = sp.copy(self.u)
        print "Done!"
        plt.imshow(self.u)
        plt.set_cmap('hot')
        plt.show()