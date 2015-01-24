# -*- coding: utf-8 -*-
"""
Created on Tue Dec  9 13:25:11 2014

@author: santiago
"""

class Material(object):

    def __init__(self, young_modulus, thermal_conductivity, chemical_value):
        """This class handle the material to be simulated"""

        self.young_modulus = 21000000 #Young's modulus
        self.thermal_conductivity = 7.8 #Thermal conductivity units are W/(m K) in the SI
        self.chemical_value = 0
      
    @property
    def young_modulus(self): 
        return self.__young_modulus
    
    @young_modulus.setter
    def young_modulus(self, young_modulus):
        self.__young_modulus = young_modulus
      
    @property
    def thermal_conductivity(self):
        return self.__thermal_conductivity
    
    @thermal_conductivity.setter
    def thermal_conductivity(self, thermal_conductivity):
        self.__thermal_conductivity = thermal_conductivity
    
    @property
    def chemical_value(self):
        return self.__chemical_value
    
    @chemical_value.setter
    def chemical_value(self, chemical_value):
        self.__chemical_value = chemical_value
        
    
    