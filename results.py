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

    def thermalResults(self):
        heatmap = np.zeros(self.materials.shape)

        for i in range(self.materials.shape[0]):
            for j in range(self.materials.shape[1]):
                heatmap[i,j] = self.materials[i,j].temperature

        plt.imshow(heatmap)
#        plt.imshow(heatmap, cmap=cm.jet, interpolation='nearest', origin='lower')
#        plt.axis([heatmap.min(), heatmap.max(), heatmap.min(), heatmap.max()])
        plt.colorbar()
        plt.show()