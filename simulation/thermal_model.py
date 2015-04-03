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
from physical_model import PhysicalModel

class ThermalModel(PhysicalModel):
    def __init__(self, matrix_materials, meanTC):
        r"""
        This class provides the thermal model through  two-dimensional
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

        :param matrix_materials: numpy array object which represents
            the whole toy model
        :type matrix_materials: 3d numpy array of Material objetcs
        :param float maxTC: maximum transfer coefficient among the different
            materials, used to define stability of dt in the scheme

        .. note::
            Part of the code in this class is based on the `examples`_ developed by
            Timothy A.V. Teatro licensed under `Creative Commons`_

        .. _examples: http://www.timteatro.net/2010/10/29/performance-python-solving-the-2d-diffusion-equation-with-numpy/
        .. _Creative Commons: http://creativecommons.org/licenses/by-sa/2.0/
        """

        super(ThermalModel, self).__init__(matrix_materials)

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
        dx = 10./self.lengthX
        dy = 10./self.lengthY
        self.dx2 = dx**2 # To save CPU cycles, we'll compute Delta x^2
        self.dy2 = dy**2 # and Delta y^2 only once and store them.
        print "dx2=", self.dx2
        print "dy2=", self.dy2

        # For stability, this is the largest interval possible
        # for the size of the time-step:
        print meanTC
        self.dt = self.dx2*self.dy2/(2*7.8*(self.dx2 + self.dy2))
        print "dt = ", self.dt
        
        internal_temp=15
        self.ui.fill(internal_temp)    # internal temperature in asphalt


    def applySimulationConditions(self, env_temp=40, internal_temp=10):
        r"""
        Set the temperatures in the matrix materials, that is, the environmental
        temperature (boundary condition) and the initial internal temperature
        in the toy model

        :param float env_temp: the environmental temperature
        :param float internal_temp: the initial internal temperature to apply in
            the toy model
        """
        env_temp=40

        self.ui[:2,:] = env_temp # applied temperature from environment
        self.ui[-2:,:] = env_temp
        self.ui[:,:2] = env_temp
        self.ui[:,-2:] = env_temp

#        print "Applied internal temperature in the asphalt:", internal_temp
#        print "Applied temperature from environment:", env_temp

    def simulate(self, n_steps):
        r"""
        This function simulates the difussion in the given number of steps.

        :param integer n_steps: number of steps in which the diffusion model runs
        :return: the matrix materials updated
        :rtype: 3d numpy array of Material objetcs
        """

        steps = np.arange(n_steps)
        start_time = time.time()  # Measures file loading time

        for step in np.nditer(steps):
            self.applySimulationConditions()
            print "Thermal simulation step:", step
            self. u = laplacian.evolve_ts(self.ui, self.u, self.TCs,
                                self.dt, self.dx2, self.dy2)
            
            arr = self.ui[1:-1, 1:-1]
            if (arr>39).all() :
                "entro"
                print "final step is ", step
                print "each steap equal to ", step/14400., "seconds"
                break
            
            self.ui = self.u.copy()

        # copy the field temperature into the matrix materials
        for i in xrange(self.MM.shape[0]):
            for j in xrange(self.MM.shape[1]):
                self.MM[i,j].temperature = self.u[i,j]

        end_time = time.time()  # Get the time when method ends
#        print "Thermal simulation done in ", str(end_time - start_time), " seconds."

        return self.MM
