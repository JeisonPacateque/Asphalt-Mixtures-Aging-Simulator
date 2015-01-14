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
    def __init__(self, sample, const, ui, u, parent=None):
        super(ThermalModel, self).__init__(parent)
        
        self.sample = sample
        self.const = const # matriz de constantes de conductividad
        self.ui = ui # matriz inicial de temp
        self.u = u # matriz inicial de temp
        
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
        self.button = QtGui.QPushButton('Plot')
        self.button.clicked.connect(self.empieza)
        
        self.pbutton = QtGui.QPushButton('Pausa')
        self.pbutton.clicked.connect(self.para)

        # set the layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        layout.addWidget(self.pbutton)
        self.setLayout(layout)
        
    
    @staticmethod
    def loadSample():
        import file_loader
        import segmentation
        
        Loader = file_loader.FileLoader()
        Seg = segmentation.Segmentation()
        
        path = "samples/4"
        collection = Loader.load_path(path) #Load Files
        print str(len(collection))+" DICOM files loaded."
            
        scaled = Seg.reduction(collection)
        toymodel = Seg.segment_all_samples(scaled)
        
        sample = toymodel[:, :, 50].transpose()
        return sample
        
    def empieza(self):
        self.timer.start(150)
        QtCore.QObject.connect(self.timer,QtCore.SIGNAL("timeout()"), self.updatefig)
   
    def para(self):
        self.timer.stop()
        
    def get_a(self, i, j):
        return self.const[i, j]
    
    def evolve_ts(self, u, ui):
        """
        This function uses two plain Python loops to
        evaluate the derivatives in the Laplacian, and
        calculates u[i,j] based on ui[i,j].
        """
        for i in range(1,u.shape[0]-1):
            for j in range(1,u.shape[1]-1):
                uxx = ( ui[i+1,j] - 2*ui[i,j] + ui[i-1, j] )/dx2
                uyy = ( ui[i,j+1] - 2*ui[i,j] + ui[i, j-1] )/dy2
                a = self.get_a(i, j)
                u[i,j] = ui[i,j]+dt*a*(uxx+uyy)
        return ui
                
    def updatefig(self):

        f=self.figure
        f.clf()
        f.add_subplot(111)
        plt.hold(False)
        plt.imshow(self.ui, cmap=cm.hot , interpolation='nearest', origin='lower')
        plt.colorbar()
        
        f.add_subplot(121)
        plt.imshow(self.sample, cmap=cm.seismic , interpolation='nearest', origin='lower')
        plt.colorbar()

        self.canvas.draw()
        
        self.ui = self.evolve_ts(self.u, self.ui)
        
        self.ui = sp.copy(self.u)
        self.iteration+=1
        print "Computing and rendering u for m =", self.iteration
        
        if self.iteration >= timesteps:
            return False
        return True        

#-----------------------------------------------------------------------------.
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    sample = ThermalModel.loadSample()
    const = np.empty((sample.shape)) # matriz de constantes de conductividad
    ui = np.zeros((sample.shape)) # matriz inicial de temp   
    u = np.zeros((sample.shape)) # matriz inicial de temp
    
    main = ThermalModel(sample, const, ui, u)
    main.show()
    
    print "sample shape", main.sample.shape
    print "const shape", main.const.shape
    print "shape ui", main.ui.shape    
    print "shape u", main.u.shape    
    
    #Thermal conductivity units are W/(m K) in the SI 
    #system and Btu/(hr ft °F) in the Imperial system.
    conductAsphalt = 0.75
    conductAir = 0.026
    conductRock = 7.8
    
    for (x,y), value in np.ndenumerate(main.sample):
        if main.sample[x, y] == 2:
            main.const[x, y] = conductRock
        elif main.sample[x, y] == 1: 
            main.const[x, y] = conductAsphalt
        else:
            main.const[x, y] = conductAir
    
    #dx=0.01        # Interval size in x-direction.
    #dy=0.01        # Interval size in y-direction.
    #a=0.5          # Diffusion constant.
    
    timesteps=500  # Number of time-steps to evolve system.
    
    #nx = 
    #ny = int(1/dy)
    dx = 1./sample.shape[0]
    dy = 1./sample.shape[1]
    dx2=dx**2 # To save CPU cycles, we'll compute Delta x^2
    dy2=dy**2 # and Delta y^2 only once and store them.
    print "dx2=", dx2
    print "dy2=", dy2
    
    # For stability, this is the largest interval possible
    # for the size of the time-step:
    dt = dx2*dy2/(conductRock**(dx2+dy2) )
    
    main.ui[-10:-1, :] = 100 #condicion inicial
    
    
    sys.exit(app.exec_())