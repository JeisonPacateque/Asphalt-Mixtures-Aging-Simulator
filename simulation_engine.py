# -*- coding: utf-8 -*-
"""
Created on Fri Jan 16 20:33:56 2015

@author: Kmy
"""
from thermal_model import ThermalModel
from fem_mechanics import FEMMechanics

class SimulationEngine(object):
    def __init__(self, Material):
        self.Material = Material
        self.Thermal = ThermalModel(self.Material)
        self.Mechanics = FEMMechanics(self.Material)

        self.Mechanics.runSimulation()
        self.Thermal.runSimulation()
