# -*- coding: utf-8 -*-
"""
Author: Timothy A.V. Teatro <http://www.timteatro.net>
Date  : Oct 25, 2010
Lisence: Creative Commons BY-SA
(http://creativecommons.org/licenses/by-sa/2.0/)

Description:
    A program which uses an explicit finite difference
    scheme to solve the diffusion equation with fixed
    boundary values and a given initial value for the
    density u(x,y,t). This version uses a numpy
    expression which is evaluated in C, so the
    computation time is greatly reduced over plain
    Python code.

    This version also uses matplotlib to create an
    animation of the time evolution of the density.
"""
from __future__ import division
import scipy as sp
import numpy as np
import matplotlib
matplotlib.use('GTKAgg') # Change this as desired.
import gobject
from pylab import *

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
    
    tajada = toymodel[:, :, 50]
    return tajada
    
tajada = loadSample()
print "tajada shape", tajada.shape
const = np.empty((tajada.shape)) # matriz de constantes de conductividad
print "const shape", const.shape
ui = np.zeros((tajada.shape)) # matriz inicial de temp
print "shape ui", ui.shape
u = np.zeros((tajada.shape)) # matriz inicial de temp
print "shape u", u.shape

#Thermal conductivity units are W/(m K) in the SI 
#system and Btu/(hr ft °F) in the Imperial system.
conductAsphalt = 0.75
conductAir = 0.026
conductRock = 7.8

for (x,y), value in np.ndenumerate(tajada):
    if tajada[x, y] == 2:
        const[x, y] = conductRock
    elif tajada[x, y] == 1: 
        const[x, y] = conductAsphalt
    else:
        const[x, y] = conductAir

#dx=0.01        # Interval size in x-direction.
#dy=0.01        # Interval size in y-direction.
#a=0.5          # Diffusion constant.

timesteps=500  # Number of time-steps to evolve system.

#nx = 
#ny = int(1/dy)
dx = 1/tajada.shape[0]
dy = 1/tajada.shape[1]
dx2=dx**2 # To save CPU cycles, we'll compute Delta x^2
dy2=dy**2 # and Delta y^2 only once and store them.
print dx2, dy2

# For stability, this is the largest interval possible
# for the size of the time-step:
dt = dx2*dy2/(conductRock**(dx2+dy2) )

ui[-10:-1, :] = 100 #condicion inicial

def get_a(i, j):
    return const[i, j]
    
def evolve_ts(u, ui):
    """
    This function uses two plain Python loops to
    evaluate the derivatives in the Laplacian, and
    calculates u[i,j] based on ui[i,j].
    """
    for i in range(1,u.shape[0]-1):
        for j in range(1,u.shape[1]-1):
            uxx = ( ui[i+1,j] - 2*ui[i,j] + ui[i-1, j] )/dx2
            uyy = ( ui[i,j+1] - 2*ui[i,j] + ui[i, j-1] )/dy2
            a = get_a(i, j)
            u[i,j] = ui[i,j]+dt*a*(uxx+uyy)
    

def updatefig(*args):
    global u, ui, m
    im.set_array(ui)
    manager.canvas.draw()
    # Uncomment the next two lines to save images as png
    # filename='diffusion_ts'+str(m)+'.png'
    # fig.savefig(filename)
    evolve_ts(u, ui)
#    u[1:-1, 1:-1] = ui[1:-1, 1:-1] + a*dt*(
#        (ui[2:, 1:-1] - 2*ui[1:-1, 1:-1] + ui[:-2, 1:-1])/dx2
#        + (ui[1:-1, 2:] - 2*ui[1:-1, 1:-1] + ui[1:-1, :-2])/dy2 )
    ui = sp.copy(u)
    m+=1
    print "Computing and rendering u for m =", m
    if m >= timesteps:
        return False
    return True

fig = plt.figure(1)
img = subplot(111)
im = img.imshow( ui, cmap=cm.hot, interpolation='nearest', origin='lower')
manager = get_current_fig_manager()

m=1
fig.colorbar( im ) # Show the colorbar along the side

# once idle, call updatefig until it returns false.
gobject.idle_add(updatefig)
show()