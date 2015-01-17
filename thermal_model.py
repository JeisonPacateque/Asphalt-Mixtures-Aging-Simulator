# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 00:01:43 2015

@author: santiago
"""
import sys
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from PyQt4 import QtGui, QtCore
from pylab import cm
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar


class ThermalModel(QtGui.QDialog):
    def __init__(self, Material, parent=None):
        super(ThermalModel, self).__init__(parent)

        self.material = Material
        self.sample = self.material.loadVerticalSlice().transpose()
        self.thermicalConstantsMatrix = self.material.thermicalConstantsMatrix.transpose() # matriz de thermicalConstantsMatrixantes de conductividad
        self.ui = np.zeros((self.sample.shape)) # matriz inicial de temp
        self.u = np.zeros((self.sample.shape)) # matriz inicial de temp
#        self._want_to_close = False #Qt variable for detect close event

    def runSimulation(self):
        print "Running thermical simulation..."
        self.applySimulationConditions()
        self.iteration = 0

        self.timer = QtCore.QTimer(self)
        self.timerTime = 0

        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.button = QtGui.QPushButton('Start')
        self.button.clicked.connect(self.start)

        self.pbutton = QtGui.QPushButton('Pause')
        self.pbutton.clicked.connect(self.stop)

        # set the layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        layout.addWidget(self.pbutton)
        self.setLayout(layout)

        #Calculate dx, dy
        self.dx = 1./self.sample.shape[0]
        self.dy = 1./self.sample.shape[1]
        self.dx2=self.dx**2 # To save CPU cycles, we'll compute Delta x^2
        self.dy2=self.dy**2 # and Delta y^2 only once and store them.
        print "dx2=", self.dx2
        print "dy2=", self.dy2

        # For stability, this is the largest interval possible
        # for the size of the time-step:
        self.dt = self.dx2*self.dy2/(self.material.conductRock**(self.dx2+self.dy2) )
        self.show()

    def applySimulationConditions(self, ambient=20, applied=100):
        """"Set the temperatures for the simulation """
        self.ui.fill(ambient)    #temperatura ambiente
        self.ui[-10:, :] = applied #temperatura aplicada
        print "Applyed temperature over asphalt:", applied
        print "Ambient temperature:", ambient

    def start(self):
        """Begin the simulation"""
        self.timer.start(150)
        QtCore.QObject.connect(self.timer,QtCore.SIGNAL("timeout()"), self.updatefig)

    def stop(self):
        """Pause the current simulation"""
        self.timer.stop()

    def get_a(self, i, j):
        """Method to get an specific index of the thermal coeficients"""
        return self.thermicalConstantsMatrix[i, j]

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

    def updatefig(self):
        """"Show the evolution of the thermical simulation"""
        self.figure.clf()
        self.figure.add_subplot(111)
        plt.hold(False)
        plt.imshow(self.ui, cmap=cm.seismic , interpolation='nearest', origin='lower')
        plt.colorbar()

        self.figure.add_subplot(121)
        plt.imshow(self.sample, cmap=cm.seismic , interpolation='nearest', origin='lower')
        plt.colorbar()

        self.canvas.draw()

        self.ui = self.evolve_ts(self.u, self.ui)

        self.ui = sp.copy(self.u)
        self.iteration+=1
        print "Computing and rendering thermal diffussion step", self.iteration

    def closeEvent(self, evnt):
        """Interrupt the execution of the simulation when the dialog is closed"""
        self.stop()

