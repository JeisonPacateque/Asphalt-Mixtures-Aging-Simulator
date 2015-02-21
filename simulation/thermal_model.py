'''
..  Copyright (C) 2015 Jeison Pacateque, Santiago Puerto

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
import time
import laplacian

class ThermalModel(object):
    def __init__(self, matrix_materials, max_TC=7.8):
        r"""
        Provides the thermal model through  two-dimensional
        difussion:

        :Definition:

        .. math::
            \frac{\partial u}{\partial t} = a \left ( \frac{\partial^2 u}
            {\partial^2 x^2} + \frac{\partial^2 u}{\partial^2 y^2} \right )

        Applying a finite forward difference approximations to the derivatives,
        it is obtained the following discrete function:

        .. math::
            U^{(m+1)}_{i,j} = U_{i,j}^{(m)} + a\Delta t \left(
            \frac{U_{i+1,j}^{(m)} - 2u_{i,j}^{(m)} + u_{i-1,j}^{(m)}}
            {(\Delta x)^2} + \frac{U_{i,j+1}^{(m)} - 2u_{i,j}^{(m)} +
            u_{i,j-1}^{(m)}}{(\Delta y)^2} \right)
        
        To avoid noise in the solution, it is necessary to ensure the following
        stability criteria:

        .. math::
            \Delta t \leq \frac{1}{2a} \frac{(\Delta x \Delta y)^2}
            {(\Delta x)^2 + (\Delta x)^2}

        :Arguments:
            - matrix_materials
            - maxTC

        matrix_materials = initial matrix materials
        (numpy objetc array, array of class Material)

        maxTC = max transfer coefficient, important to define stability
        of dt in the model
        """

        # reference of the matrix materials used only
        # to get transfer coeefficient amd  object construction
        self.MM  = matrix_materials.copy()

        #initial temperature field
        self.ui = np.zeros(self.MM.shape, dtype=np.float)
        self.u = self.ui.copy() # next step temperature field
        self.TCs = np.zeros(self.MM.shape, dtype=np.float)

#         copy all the thermal conductivities from the matrix materials
        for i in xrange(self.MM.shape[0]):
                for j in xrange(self.MM.shape[1]):
                    self.TCs[i,j] = self.MM[i,j].thermal_conductivity

        # Calculate dx, dy
        self.lengthX = self.MM.shape[0]
        self.lengthY = self.MM.shape[1]
        dx = 1./self.lengthX
        dy = 1./self.lengthY
        self.dx2 = dx**2 # To save CPU cycles, we'll compute Delta x^2
        self.dy2 = dy**2 # and Delta y^2 only once and store them.
        print "dx2=", self.dx2
        print "dy2=", self.dy2

        # For stability, this is the largest interval possible
        # for the size of the time-step:
        self.dt = self.dx2*self.dy2/(max_TC**(self.dx2 + self.dy2))
        print "dt = ", self.dt

    def applySimulationConditions(self, ambient=40, internal=10):
        """"Set the temperatures for the simulation"""

        self.ui.fill(internal)    # internal temperature in asphalt
        self.ui[:10,:] = ambient # applied temperature from environment

        print "Applied internal temperature in the asphalt:", internal
        print "applied temperature from environment:", ambient

    def simulate(self, n_steps):
        """"This function executes the model in number steps (n_steps)"""

        steps = np.arange(n_steps)
        start_time = time.time()  # Measures file loading time

        for step in np.nditer(steps):
            print "Thermal simulation step:", step
            self. u = laplacian.evolve_ts(self.ui, self.u, self.TCs,
                                self.dt, self.dx2, self.dy2)
            self.ui = self.u.copy()

        # copy the field temperature into the matrix materials
        for i in xrange(self.MM.shape[0]):
            for j in xrange(self.MM.shape[1]):
                self.MM[i,j].temperature = self.u[i,j]

        end_time = time.time()  # Get the time when method ends
        print "Thermal simulation done in ", str(end_time - start_time), " seconds."
        return self.MM