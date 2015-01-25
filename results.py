# -*- coding: utf-8 -*-
"""
Created on Sun Jan 25 16:21:14 2015

@author: sjdps
"""
import matplotlib.pyplot as plt
import numpy as np

class Result(object):
    def __init__(self, matrix_materials):
        self.materials = matrix_materials
        print "results"

    def thermalResults(self):
        thermal_map = np.empty(self.materials.shape, dtype=float)

        for i in range(self.materials.shape[0]):
            for j in range(self.materials.shape[1]):
                thermal_map[i,j] = self.materials[i,j].temperature

        plt.imshow(thermal_map)
#        plt.set_cmap('hot')
        plt.show()