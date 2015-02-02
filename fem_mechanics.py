# -*- coding: utf-8 -*-
"""
Created on Tue Nov 25 09:31:31 2014

@author: santiago
"""

import numpy as np
import time
from matplotlib import pyplot, colors


class FEMMechanics(object):
    def __init__(self, matrix_materials):
        """This class supports the Mechanic FEM Simulation
        matrix_materials = initial matrix materials
        (numpy objetc array, array of class Material)
        """
        self.MM = matrix_materials # local reference of the matrix materials

        self.ki = np.zeros((self.MM.size)) # Create stiffness matrix
        cont = 0
        for m in np.nditer(self.MM):
            self.ki[cont] = self.LinearBarElementStiffness(m.young_modulus,\
            m.areaFE, m.lengthFE)
            cont += 1

        self.elements_nodes = []  # Tupla de nodos de cada elemento
        self.elements_top = [] # Indice Elemento superior
        self.elements_bottom = [] #Indice Elemento inferior

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

    def simulate(self):
        print "Running mechanic simulation..."
        start_time = time.time()  # Measures Stiffness Assemble matrix time

        # Carga del Slice-----------------------------------------------
        sample = self.material.vertical_slice
        slice_size = sample.shape

        #Obtencion de los nodos superiores e inferiores--------------------
        top_nodes = self.conectivity.getTopElementNodes()
        bottom_nodes = self.conectivity.getBottomElementNodes()

        self.ki = self.material.ki
        self.K = self.material.K

        mask = np.ones(self.K.shape[0], dtype=bool)
        mask[bottom_nodes] = False
        k_sub = self.K[mask]
        k_sub = k_sub[:, mask]

        #Aplicar fuerzas sobre el modelo------------------------------------
        force = 800
        Fuerzas = force * np.ones(k_sub.shape[0])

        #Calcular desplazamientos-------------------------------------------
        U = np.linalg.solve(k_sub, Fuerzas)

        #np.set_printoptions(suppress=True)
        img = U.reshape(slice_size).transpose()

        #Guardar desplazamientos--------------------------------------------
        # turn off summarization, line-wrapping
        np.set_printoptions(threshold=np.inf, linewidth=np.inf)
        with open('matriz_u.txt', 'w') as f:
            f.write(np.array2string(img, separator=', '))

        #Mostrar desplazamientos--------------------------------------------
        f = pyplot.figure()
        f.add_subplot(111)
        pyplot.title('Displacements Map')
        pyplot.imshow(img, interpolation='nearest')
        pyplot.colorbar()

        f.add_subplot(121)
        pyplot.title('Original Slice')
        pyplot.imshow(sample.transpose(), interpolation='nearest')
        pyplot.colorbar()
        pyplot.show()

        end_time = time.time()  # Get the time when method ends
        print "Displacements done and saved in",
        str(end_time - start_time), "seconds."

        print "Top nodes:", len(top_nodes)
        print "Bottom nodes:", len(bottom_nodes)

    def LinearBarElementStiffness(self, E, A, L):
        """ This function returns the element stiffness"""
        return np.array([[E*(A/L), -E*(A/L)], [-E*(A/L) ,E*(A/L)]])

    def generalStiffnessMatrixAssemble(self, slice_size):
        """Assembles an n x n Stiffness Matrix"""
        start_time = time.time()  # Measures Stiffness Assemble matrix time
        #Creacion de la matriz de conectividad------------------------

        con_mtrx = self.conectivity.ElementConectivityMatrix(slice_size[0],
                                                             slice_size[1])
        self.K = np.zeros((4600, 4600))

        cont = 0
        for y in con_mtrx:
            self.K = self.LinearBarAssemble(self.K, self.ki[cont], y[0], y[1])
            cont = cont+1

#        print "General Stiffness Matriz shape:", self.K.shape

        end_time = time.time()  # Get the time when method ends
        print "General Stiffness Matriz done in",
        str(end_time - start_time), "seconds."
        return self.K

    def LinearBarAssemble(self, K, k, i, j):
        """This function assembles the element stiffness matrix k of the linear
        bar with nodes i and j into the global stiffness matrix K.This function
        returns the global stiffness matrix K after the element stiffness
        matrix k is assembled."""
        K[i][i] = K [i][i] + k[0][0]
        K[i][j] = K [i][j] + k[0][1]
        K[j][i] = K [j][i] + k[1][0]
        K[j][j] = K [j][j] + k[1][1]
        return K

    def ElementConectivityMatrix(self, width, height):
        """Create the nodes and set positions for all elements
        on a stiffness matrix"""

        a = 0
        b = 1
        for i in range(width):
            self.elements_top.append(a)
            for j in range(height):
                self.elements_nodes.append((a, b))
                a=a+1
                b=b+1
            self.elements_bottom.append(b-1)
            a=a+1
            b=b+1

        print "Conectivity matrix done in",
        str(end_time - start_time), "seconds."
        return self.elements_nodes

    def getTopElementNodes(self):
        return self.elements_top

    def getBottomElementNodes(self):
        return self.elements_bottom