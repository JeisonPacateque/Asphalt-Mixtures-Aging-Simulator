# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod 

class PhysicalModel(object):
    __metaclass__ = ABCMeta
    
    def __init__(self, matrix_materials):
        self.MM = matrix_materials # local reference of the matrix materials
    
    @abstractmethod
    def applySimulationConditions():
        pass
    
    @abstractmethod
    def simulate():
        pass
        