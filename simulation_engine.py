# -*- coding: utf-8 -*-
"""
Created on Fri Jan 16 20:33:56 2015

@author: Santiago
"""

from thermal_model import ThermalModel
from fem_mechanics import FEMMechanics
import numpy as np
from material import Material

class SimulationEngine(object):
    def __init__(self, aggregate_parameters, mastic_parameters, 
                                  air_parameters, collection, slice_id=50):
        
        self.mastic = Material(mastic_parameters[0], mastic_parameters[1],
                               mastic_parameters[2])
        self.aggregate = Material(aggregate_parameters[0], aggregate_parameters[1],
                                   aggregate_parameters[2])
        self.airvoid = Material(air_parameters[0], air_parameters[1], 
                                air_parameters[2])

        vertical_slice = self.loadVerticalSlice(collection, slice_id=50)

        self.matrix_materials = self.getMatrixMaterials(vertical_slice)        
     

        self.thermal = ThermalModel(self.matrix_materials)
        self.thermal.simulate()
#        self.techanics = FEMMechanics(self.material)
        
#        self.thermicalConstantsMatrix = self.assignThermicalProperties(self.vertical_slice)
#        self.assignMechanicalProperties(self.vertical_slice)
#        self.generalStiffnessMatrixAssemble(self.vertical_slice.shape)
        
        
    def loadVerticalSlice(self, collection, slice_id):
        """Cut the central slice of the sample for FEM mechanics simulation"""
        vertical = collection[:, :, slice_id]
        return vertical
    
    def getMatrixMaterials(self, vertical_slice):
        material_matrix = np.empty(vertical_slice.shape, dtype=object)
        for (x,y), value in np.ndenumerate(vertical_slice):
            if vertical_slice[x, y] == 2:
                material_matrix[x, y] = self.aggregate
            elif vertical_slice[x, y] == 1: 
                material_matrix[x, y] = self.mastic
            else:
                material_matrix[x, y] = self.airvoid
        
        return material_matrix
            
    
        
    def assignMechanicalProperties(self, sample):
        """Load the sample and assing the material modulus for each pixel detected"""
        start_time = time.time()  # Measures Stiffness Assemble matrix time
        self.ki = np.empty(sample.size, dtype=object)#Creacion de la matriz de rigidez vacia
#        print "Loaded slice shape:", sample.shape
        cont=0
        
        for x in np.nditer(sample):
        #    print x
            if x==2:
                self.ki[cont] = self.LinearBarElementStiffness(self.aggregate_YM, self.A, self.L)
            elif x==1:
                self.ki[cont] = self.LinearBarElementStiffness(self.mastic_YM, self.A, self.L)
            else:
                self.ki[cont] = self.LinearBarElementStiffness(self.air_YM, self.A, self.L)
            
            cont=cont+1

        return thermicalConstantsMatrix

