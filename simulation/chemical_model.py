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
