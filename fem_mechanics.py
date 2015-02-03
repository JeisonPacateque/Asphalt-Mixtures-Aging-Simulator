# -*- coding: utf-8 -*-
"""
Created on Tue Nov 25 09:31:31 2014

@author: santiago
"""

import numpy as np

class FEMMechanics(object):
    def __init__(self, matrix_materials):
        """This class supports the Mechanic FEM Simulation
        matrix_materials = initial matrix materials
        (numpy objetc array, array of class Material)
        """
        self.MM = matrix_materials # local reference of the matrix materials
        self.force = 0  # applied force over asphalt mixture

        self._createStiffnessMatrix()
        self._createConectivityMatrix()
        self._generalStiffnessMatrixAssemble()


    def _createStiffnessMatrix(self):
        """Create stiffness matrix"""
        self.ki = np.empty(self.MM.size, dtype=object)
        cont = 0
        for i in xrange(self.MM.shape[0]):
            for j in xrange(self.MM.shape[1]):
                self.ki[cont] = self._LinearBarElementStiffness(
                self.MM[i,j].young_modulus,\
                self.MM[i,j].areaFE, self.MM[i,j].lengthFE)
                cont += 1

    def _createConectivityMatrix(self):
        """ Create Conectivity Matrix """
        self.elements_nodes = []  # Tupla de nodos de cada elemento
        self.elements_top = [] # Indice Elemento superior
        self.elements_bottom = [] #Indice Elemento inferior
        #La matriz de conectividad se debe cargar invertida
        self.conectivity_matrix = self._ElementConectivityMatrix(
        self.MM.shape[1], self.MM.shape[0])

    def _LinearBarElementForces(self, k, u):
        """This function returns the element nodalforce vector given the
        element stiffness matrix k and the element nodal displacement
        vector u."""
        return np.dot(k, u)

    def _LinearBarElementStresses(self, k, u, A):
        """This function returns the element nodal stress vector given the
        element stiffness matrix k, the element nodal displacement vector u,
        and the cross-sectional area A."""
        y = np.dot(k, u)
        return y / A

    def _LinearBarElementStiffness(self, E, A, L):
        """ This function returns the element stiffness"""
        return np.array([[E*(A/L), -E*(A/L)], [-E*(A/L), E*(A/L)]])

    def _generalStiffnessMatrixAssemble(self):
        """Assembles an n x n Stiffness Matrix"""
        ksize = self.MM.shape[1]*(self.MM.shape[0]+1)
        self.K = np.zeros((ksize, ksize))
        cont = 0
        for (x, y) in self.conectivity_matrix:
            self.K = self._LinearBarAssemble(self.K, self.ki[cont], x, y)
            cont += 1

    def _LinearBarAssemble(self, K, k, i, j):
        """This function assembles the element stiffness matrix k of the linear
        bar with nodes i and j into the global stiffness matrix K.This function
        returns the global stiffness matrix K after the element stiffness
        matrix k is assembled."""
        K[i][i] = K[i][i] + k[0][0]
        K[i][j] = K[i][j] + k[0][1]
        K[j][i] = K[j][i] + k[1][0]
        K[j][j] = K[j][j] + k[1][1]
        return K

    def _ElementConectivityMatrix(self, width, height):
        """Create the nodes and set positions for all elements
        on a stiffness matrix"""
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

    def applySimulationConditions(self, force=800):
        self.force = force

    def simulate(self):
        mask = np.ones(self.K.shape[0], dtype=bool)
        mask[self.elements_bottom] = False
        k_sub = self.K[mask]
        k_sub = k_sub[:, mask]

        #Apply forces over model------------------------------------
        forces = self.force * np.ones(k_sub.shape[0])

        #calculate displacements-------------------------------------------
        U = np.linalg.solve(k_sub, forces)
        U = U.reshape(self.MM.shape)
        print U.shape

        # copy the field temperature into the matrix materials
        for i in xrange(self.MM.shape[0]):
            for j in xrange(self.MM.shape[1]):
                self.MM[i,j].displacement = U[i,j]