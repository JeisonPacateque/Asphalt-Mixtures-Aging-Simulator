# -*- coding: utf-8 -*-
"""
Created on Tue Nov 25 09:31:31 2014

@author: santiago
"""

import numpy as np
import time

class FEMMechanics(object):
    def __init__(self, matrix_materials):
        """This class supports the Mechanic FEM Simulation
        matrix_materials = initial matrix materials
        (numpy objetc array, array of class Material)
        """
        self.MM = matrix_materials # local reference of the matrix materials

#==============================================================================
#        Create stiffness matrix
#==============================================================================
        self.ki = np.empty(self.MM.size, dtype=object)
        cont = 0
        for i in xrange(self.MM.shape[0]):
            for j in xrange(self.MM.shape[1]):
                self.ki[cont] = self.LinearBarElementStiffness(
                self.MM[i,j].young_modulus,\
                self.MM[i,j].areaFE, self.MM[i,j].lengthFE)
                cont += 1

#==============================================================================
#       Create conectivity matrix
#==============================================================================
        self.elements_nodes = []  # Tupla de nodos de cada elemento
        self.elements_top = [] # Indice Elemento superior
        self.elements_bottom = [] #Indice Elemento inferior
        self.conectivity_matrix = self.ElementConectivityMatrix(self.MM.shape[0],
                                                           self.MM.shape[1])

        self.K = np.zeros((4600, 4600)) # estos valores hay que cambiarlos, calcularlos dependiendo
        self.generalStiffnessMatrixAssemble()

        self.force = 0  #applied force over asphalt mixture

    def LinearBarElementForces(self, k, u):
        """This function returns the element nodalforce vector given the
        element stiffness matrix k and the element nodal displacement
        vector u."""
        return np.dot(k, u)

    def LinearBarElementStresses(self, k, u, A):
        """This function returns the element nodal stress vector given the
        element stiffness matrix k, the element nodal displacement vector u,
        and the cross-sectional area A."""
        y = np.dot(k, u)
        return y / A

    def LinearBarElementStiffness(self, E, A, L):
        """ This function returns the element stiffness"""
        return np.array([[E*(A/L), -E*(A/L)], [-E*(A/L) ,E*(A/L)]])

    def generalStiffnessMatrixAssemble(self):
        """Assembles an n x n Stiffness Matrix"""
        cont = 0
        for (x, y) in self.conectivity_matrix:
            self.K = self.LinearBarAssemble(self.K, self.ki[cont], x, y)
            cont += 1

    def LinearBarAssemble(self, K, k, i, j):
        """This function assembles the element stiffness matrix k of the linear
        bar with nodes i and j into the global stiffness matrix K.This function
        returns the global stiffness matrix K after the element stiffness
        matrix k is assembled."""
        K[i][i] = K[i][i] + k[0][0]
        K[i][j] = K[i][j] + k[0][1]
        K[j][i] = K[j][i] + k[1][0]
        K[j][j] = K[j][j] + k[1][1]
        return K

    def ElementConectivityMatrix(self, width, height):
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

    def getTopElementNodes(self):
        return self.elements_top

    def getBottomElementNodes(self):
        return self.elements_bottom

    def applySimulationConditions(self, force=800):
        self.force = 800

    def simulate(self):
        # Obtencion de los nodos superiores e inferiores
        top_nodes = self.getTopElementNodes()
        bottom_nodes = self.getBottomElementNodes()

        mask = np.ones(self.K.shape[0], dtype=bool)
        mask[bottom_nodes] = False
        k_sub = self.K[mask]
        k_sub = k_sub[:, mask]

        #Apply forces over model------------------------------------
        forces = self.force * np.ones(k_sub.shape[0])

        #calculate displacements-------------------------------------------
        U = np.linalg.solve(k_sub, forces)

        #np.set_printoptions(suppress=True)
        img = U.reshape(self.MM.shape)

        #Guardar desplazamientos--------------------------------------------
        # turn off summarization, line-wrapping
        np.set_printoptions(threshold=np.inf, linewidth=np.inf)
        with open('matriz_u.txt', 'w') as f:
            f.write(np.array2string(img, separator=', '))