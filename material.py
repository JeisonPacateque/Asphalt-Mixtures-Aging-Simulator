# -*- coding: utf-8 -*-
"""
Created on Tue Dec  9 13:25:11 2014

@author: santiago
"""

class Material(object):
    def __init__(self, young_modulus, thermal_conductivity, chemical_value):
        """This class handle the material to be simulated"""

        self.young_modulus = young_modulus # Young's modulus
        # Thermal conductivity units are W/(m K) in the SI
        self.thermal_conductivity = thermal_conductivity
        self.chemical_value = chemical_value

        self.temperature = 0
        self.AreaFE = 1
        self.LengthFE = 1

    @property
    def young_modulus(self):
        return self._young_modulus

    @young_modulus.setter
    def young_modulus(self, young_modulus):
        self._young_modulus = young_modulus

    @property
    def thermal_conductivity(self):
        return self._thermal_conductivity

    @thermal_conductivity.setter
    def thermal_conductivity(self, thermal_conductivity):
        self._thermal_conductivity = thermal_conductivity

    @property
    def chemical_value(self):
        return self._chemical_value

    @chemical_value.setter
    def chemical_value(self, chemical_value):
        self._chemical_value = chemical_value

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, temperature):
        self._temperature = temperature