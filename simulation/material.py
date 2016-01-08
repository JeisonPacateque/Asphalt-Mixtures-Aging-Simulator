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

class Material(object):
    def __init__(self, phase, young_modulus, thermal_conductivity, chemical_value):
        """
        This class is the representation of the asphalt mixtures materials to
        be simulated. Since the specific nature of the intended simulations,
        just thermal mechanical and chemical attributes are considered
        """

        self._phase = phase

        self._young_modulus = float(young_modulus) # Young's modulus

        # Thermal conductivity units are W/(m K) in the SI
        self._thermal_conductivity = thermal_conductivity

        self._rca = 0  # rate carbonyle

        self._temperature = 0
        self._areaFE = 1
        self._lengthFE = 1

        self._displacement = 0 # local displacement of the element
        self._stress = 0

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

    @property
    def displacement(self):
        return self._displacement

    @displacement.setter
    def displacement(self, value):
        self._displacement = value

    @property
    def phase(self):
        return self._phase

    @phase.setter
    def phase(self, value):
        self._phase = value

    @property
    def rca(self):
        return self._rca

    @rca.setter
    def rca(self, value):
        self._rca = value

    @property
    def stress(self):
        return self._stress

    @stress.setter
    def stress(self, value):
        self._stress = value