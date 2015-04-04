# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 23:34:55 2015

@author: sjdps
"""
import numpy as np
from physical_model import PhysicalModel

class ChemicalModel(PhysicalModel):
    def __init__(self, matrix_materials):
        super(ChemicalModel, self).__init__(matrix_materials) 
        
        # temperature field in kelvins
        self.u = np.zeros(self.MM.shape, dtype=np.float)
        for i in xrange(self.MM.shape[0]):
            for j in xrange(self.MM.shape[1]):
                 self.u[i,j] = self.MM[i,j].temperature + 273.15
    
    def applySimulationConditions(self, EnergyActivation):
        self.Ea = EnergyActivation    
    
    def simulate(self):
        A = 1.21e-10  # factor de amplitud
        
        P = 14.5437 # Psi

        alfa = 0 
        
        R = 8.3144621 # molar gas constant        
        
        for i in xrange(self.MM.shape[0]):
            for j in xrange(self.MM.shape[1]):
                if self.MM[i,j].phase == 'mastic':
                    T = self.u[i,j] # temperature in the given pixel
                    self.MM[i,j].rca = A*(P**alfa)*(np.e**(-self.Ea/(R*T)))
    
        return self.MM
        