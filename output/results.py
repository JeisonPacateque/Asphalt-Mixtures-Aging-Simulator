# -*- coding: utf-8 -*-
'''
Copyright (C) 2015 Jeison Pacateque, Santiago Puerto, Wilmar Fernandez

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

import os
import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import FormatStrFormatter


class Result(object):
    def __init__(self, matrix_materials, name):
        """
        This class handle shows on screen using matplotlib the material status
        after the thermal, mechanical and chemical simulation. The thermal
        simulation results are showed through a heat map, the mechanical
        simulation results through a displacements map and the chemical reusults
        through ...
        """
        self.name = name
        self.materials = matrix_materials
        self.heatmap = self.thermalResults()
        self.stresses = self.mechanicalResults()
        self.rcas = self.chemicalResults()

    def thermalResults(self):
        """
        Heat map implementation using matplotlib
        """
        heatmap = np.zeros(self.materials.shape)

        for i in range(self.materials.shape[0]):
            for j in range(self.materials.shape[1]):
                heatmap[i,j] = self.materials[i,j].temperature

        return heatmap

    def mechanicalResults(self):
        """
        DIsplacements map implementation using matplotlib
        """
        stresses = np.zeros(self.materials.shape)

        for i in range(self.materials.shape[0]):
            for j in range(self.materials.shape[1]):
                stresses[i,j] = self.materials[i,j].stress

        return stresses

    def chemicalResults(self):
        rcas = np.zeros(self.materials.shape)
        for i in range(self.materials.shape[0]):
            for j in range(self.materials.shape[1]):
                rcas[i,j] = self.materials[i,j].rca

        return rcas


    def showResults(self):
        # Get current path
        folder_path = os.getcwd()
        # Set folder name with curent time
        timestamp = str(datetime.datetime.now().strftime('%d%m%Y_%H%M'))
        # Set the results path
        results_path = folder_path+"/results"+timestamp
        # Create forlder if results folder doesn't exist
        if not os.path.exists(results_path):
            os.makedirs(results_path)


        print("Saving the results of " + self.name)
        plt.figure(1)
        plt.clf() # clear figure
        plt.title('Heat Map')
        plt.gca().xaxis.set_major_formatter(FormatStrFormatter(u'%d Px'))
        plt.gca().yaxis.set_major_formatter(FormatStrFormatter(u'%d Px'))
        plt.xticks(rotation=45)
        plt.imshow(self.heatmap, interpolation='nearest', cmap=cm.jet, origin='lower')
        cbarHeat = plt.colorbar()
        cbarHeat.set_label(u'Celcius degrees (°C)')
        plt.savefig(results_path+"/"+self.name+"_heatmap")


#        plt.show()

        plt.figure(2)
        plt.clf()
        clines = np.linspace(0., 1., 10) # contour line levels
        plt.title('stress')
#        C = plt.contour(self.stresses, colors='k')
#        plt.clabel(C, inline=10, fontsize=10)
        plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%d Px'))
        plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%d Px'))
        plt.xticks(rotation=45)
        plt.imshow(self.stresses, interpolation='nearest', origin='lower')
        cbarStress = plt.colorbar()
        cbarStress.set_label(u'Mega Pascals (MPa)')
        plt.savefig(results_path+"/"+self.name+"_stress map")

        plt.figure(3)
        plt.clf()
        plt.title("Carbonyle rates")
#        X = plt.contour(self.rcas, colors='k')
#        plt.clabel(X, inline=10, fontsize=10)
#        plt.show()
        plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%d Px'))
        plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%d Px'))
        plt.xticks(rotation=45)
        plt.imshow(self.rcas, interpolation='nearest', origin='lower')
        cbarCarbonyle = plt.colorbar()
        cbarCarbonyle.set_label(u'Molarity/Seconds (Mol/Sec)')
        plt.savefig(results_path+"/"+self.name + "_carbonyle rates")
