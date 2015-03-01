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

import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

class Result(object):
    def __init__(self, matrix_materials):
        """
        This class handle shows on screen using matplotlib the material status
        after the thermal, mechanical and chemical simulation. The thermal
        simulation results are showed through a heat map, the mechanical
        simulation results through a displacements map and the chemical reusults
        through ...
        """
        self.materials = matrix_materials
        self.heatmap = self.thermalResults()
        self.displacements = self.mechanicalResults()

    def thermalResults(self):
        """
        Heat map implementation using matplotlib
        """
        heatmap = np.zeros(self.materials.shape)

        for i in xrange(self.materials.shape[0]):
            for j in xrange(self.materials.shape[1]):
                heatmap[i,j] = self.materials[i,j].temperature

        return heatmap

    def mechanicalResults(self):
        """
        DIsplacements map implementation using matplotlib
        """
        displacements = np.zeros(self.materials.shape)

        for i in xrange(self.materials.shape[0]):
            for j in xrange(self.materials.shape[1]):
                displacements[i,j] = self.materials[i,j].displacement

        return displacements
    
    def showResults(self):
        plt.figure(1)
        plt.clf() # clear figure
        plt.title('Heat Map')
        plt.imshow(self.heatmap, interpolation='nearest', cmap=cm.jet)
        plt.colorbar()
        plt.show()

        plt.figure(2)
        plt.clf()
        clines = np.linspace(0., 1., 10) # contour line levels
        plt.title('Displacements field')
        C = plt.contour(self.displacements, colors='k')
        plt.clabel(C, inline=10, fontsize=10)
        plt.show()