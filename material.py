# -*- coding: utf-8 -*-
"""
Created on Tue Dec  9 13:25:11 2014

@author: santiago
"""

class Material(object):
    def __init__(self, young_modulus, thermal_conductivity, chemical_value):
        """This class handle the material to be simulated"""

        self._young_modulus = float(young_modulus) # Young's modulus
        # Thermal conductivity units are W/(m K) in the SI
        self._thermal_conductivity = float(thermal_conductivity)
#        self._chemical_value = float(chemical_value)

        self._temperature = 0
        self._areaFE = 1
        self._lengthFE = 1

    @property
    def young_modulus(self):
        return self._young_modulus

    @young_modulus.setter
    def young_modulus(self, value):
        self._young_modulus = value

    @property
    def thermal_conductivity(self):
        return self._thermal_conductivity

    @thermal_conductivity.setter
    def thermal_conductivity(self, value):
        self._thermal_conductivity = value

    @property
    def chemical_value(self):
        return self._chemical_value

    @chemical_value.setter
    def chemical_value(self, value):
        self._chemical_value = value

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        self._temperature = value

    @property
    def areaFE(self):
        return self._areaFE

    @areaFE.setter
    def areFE(self, value):
        self._areaFE = value

    @property
    def lengthFE(self):
        return self._lengthFE

    @lengthFE.setter
    def lengthFE(self, value):
        self._lengthFE = value