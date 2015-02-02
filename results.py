# -*- coding: utf-8 -*-
"""
Created on Sun Jan 25 16:21:14 2015

@author: sjdps
"""
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

class Result(object):
    def __init__(self, matrix_materials):
        self.materials = matrix_materials

        f = plt.figure()
        f.add_subplot(111)
        plt.title('Heat Map')
        heatmap = self.thermalResults()
        plt.imshow(heatmap, interpolation='nearest')
        plt.colorbar()

        f.add_subplot(121)
        clines = np.linspace(0., 1., 10)
        C = plt.contour(heatmap)
        plt.clabel(C, inline=10, fontsize=10)
        plt.title('Displacements field')
#        displacements = self.mechanicalResults()
#        plt.imshow(displacements, interpolation='nearest')
#        plt.colorbar()
        plt.show()

    def thermalResults(self):
        heatmap = np.zeros(self.materials.shape)

        for i in xrange(self.materials.shape[0]):
            for j in xrange(self.materials.shape[1]):
                heatmap[i,j] = self.materials[i,j].temperature

        return heatmap

    def mechanicalResults(self):
        return np.loadtxt('matriz_u.txt', delimiter=',')
