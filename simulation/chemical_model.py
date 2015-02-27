# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 23:34:55 2015

@author: sjdps
"""

from physical_model import PhysicalModel

class ChemicalModel(PhysicalModel):
    def __init__(self, matrix_materials):
        super(ChemicalModel, self).__init__(matrix_materials) 