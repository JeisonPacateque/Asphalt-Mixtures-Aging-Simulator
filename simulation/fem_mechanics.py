'''
Copyright (C) 2015 Jeison Pacateque, Santiago Puerto

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
import time


class FEMMechanics(PhysicalModel):
    def __init__(self, matrix_materials):
        """This class supports the Mechanic FEM Simulation
        matrix_materials = initial matrix materials
        (numpy objetc array, array of class Material)        """
        
        super(FEMMechanics, self).__init__(matrix_materials)        
        
        self.force = 0  # applied force over asphalt mixture

        self._createStiffnessMatrix()
        self._createConectivityMatrix()
        self._generalStiffnessMatrixAssemble()


    def _createStiffnessMatrix(self):
        r"""This function uses the LinearBarElementStiffness to create the
        stiffness matrix (ki) for each Finite Element to create regarding
        the matrix materials (MM) it also configures each FE element with
        their Young's Modulus and their transversal area
        """
        self.ki = np.empty(self.MM.size, dtype=object)
        cont = 0
        for i in xrange(self.MM.shape[0]):
            for j in xrange(self.MM.shape[1]):
                self.ki[cont] = self._LinearBarElementStiffness(
                self.MM[i,j].young_modulus,\
                self.MM[i,j].areaFE, self.MM[i,j].lengthFE)
                cont += 1

    def _createConectivityMatrix(self):
        r"""This function initialices the conectivity_matrix object using
        the matrix materials (MM) size for reference, additionally, this
        method declares the lists where the top and bottom nodes will
        be
        """
        self.elements_nodes = []  # Tupla de nodos de cada elemento
        self.elements_top = [] # Indice Elemento superior
        self.elements_bottom = [] #Indice Elemento inferior
        #La matriz de conectividad se debe cargar invertida
        self.conectivity_matrix = self._ElementConectivityMatrix(self.MM.shape[1],
                                                                 self.MM.shape[0])

    def _LinearBarElementForces(self, k, u):
        r"""This function returns the element nodalforce vector given the
        element stiffness matrix k and the element nodal displacement
        vector u."""
        return np.dot(k, u)

    def _LinearBarElementStresses(self, k, u, A):
        r"""This function returns the element nodal stress vector given the
        element stiffness matrix k, the element nodal displacement vector u,
        and the cross-sectional area A."""
        return np.dot(k, u/A)

    def _LinearBarElementStiffness(self, E, A, L):
        r""" This function returns the Finite Element stiffness considering
        the material Young's modulus (E), the transversal area of the FE (A)
        and the length of the FE (L)

        :Definition:

        .. math::
            k= \begin{bmatrix} \frac{EA}{L}  & -\frac{EA}{L} \\ -\frac{EA}{L}
                & \frac{EA}{L} \end{bmatrix}
        """
        return np.array([[E*(A/L), -E*(A/L)], [-E*(A/L), E*(A/L)]])

    def _generalStiffnessMatrixAssemble(self):
        r"""Assembles the General Stiffness Matrix (K) using the size of the
        matrix materials (MM) as reference. It also uses the conectivity matrix
        (conectivity_matrix) to asseble the FE for every material on the matrix
        materials (MM) by using the function _LinearBarAssemble
        order to locate all the FE in place for simulation
        """
        ksize = self.MM.shape[1]*(self.MM.shape[0]+1)
        self.K = np.zeros((ksize, ksize))
        cont = 0
        for (x, y) in self.conectivity_matrix:
            self.K = self._LinearBarAssemble(self.K, self.ki[cont], x, y)
            cont += 1

    def _LinearBarAssemble(self, K, k, i, j):
        r"""This function assembles the element stiffness matrix k of the linear
        bar with nodes i and j into the global stiffness matrix K.This function
        returns the global stiffness matrix K after the element stiffness
        matrix k is assembled."""
        K[i][i] = K[i][i] + k[0][0]
        K[i][j] = K[i][j] + k[0][1]
        K[j][i] = K[j][i] + k[1][0]
        K[j][j] = K[j][j] + k[1][1]
        return K

    def _ElementConectivityMatrix(self, width, height):
        r"""This function create the nodes and set positions for all
        elements on a stiffness matrix. It also it also aggregate the
        top and bottom elements to their own list declared at the
        function _CreateConectivityMatrix
        """
        a = 0
        b = 1
        for i in xrange(width):
            self.elements_top.append(a)
            for j in xrange(height):
                self.elements_nodes.append((a, b))
                a=a+1
                b=b+1
            self.elements_bottom.append(b-1)
            a=a+1
            b=b+1

        return self.elements_nodes

    def applySimulationConditions(self, force):
        r"""
        Set the force parameter to apply over the top elements of the
        FE General Stiffness Matrix (K)
        """
        self.force = force

    def simulate(self):
        r"""
        Run the simulation with all the configured parameters, the output will
        be a displacements map handled by the results module.
        Once the global stiffness matrix K is obtained we have the following
        structure equation:

        :Definition:

        .. math::

            \left[K\right]\left\{U\right\}=\left\{F\right\}

        where U is the global nodal displacement vector and F is the global
        nodal force vector.At this step the boundary conditions are applied
        manually to the vectors U and F.

        Then the matrix is solved by partitioning and Gaussian elimination.
        Finally once the unknown displacements and reactions are found, the
        element forces are obtained for each element as follows:

        .. math::

            \left [ f \right ]  = \left [ k \right ] \left \{ u \right \}

        where f is the 2x1 element force vector and u is the 2x1 element
        displacement vector. The element stresses are obtained by dividing
        the element forces by the crosssectional area A.
        """
        start_time = time.time()  # Measures file loading time
        print "Applied force:", self.force

        mask = np.ones(self.K.shape[0], dtype=bool)
        mask[self.elements_bottom] = False
        k_sub = self.K[mask]
        k_sub = k_sub[:, mask]

        #Apply forces over model------------------------------------
        forces = self.force * np.ones(k_sub.shape[0])

        #calculate displacements-------------------------------------------
        U = np.linalg.solve(k_sub, forces)
        
        #Calculate the stress in each element
        stresses = np.zeros(U.size)
        cont = 0
        for ux in np.nditer(U):
            sigma =  self._LinearBarElementStresses(self.ki[cont], ux, 1)
            stresses[cont] = sigma[0][0]
            cont += 1
        
#        U = U.reshape(self.MM.shape) # reshape the displacements matrix U
        
        #copy the displacements field into the matrix materials
#        for i in xrange(self.MM.shape[0]):
#            for j in xrange(self.MM.shape[1]):
#                self.MM[i,j].displacement = U[i,j]    
        
        stresses = stresses.reshape(self.MM.shape)
        #copy the stresses field into the matrix materials
        for i in xrange(self.MM.shape[0]):
            for j in xrange(self.MM.shape[1]):
                self.MM[i,j].stress = stresses[i, j]  
        
        end_time = time.time()  # Get the time when method ends
        print "Mechanical simulation done in ", str(end_time - start_time), " seconds."
        
        return self.MM