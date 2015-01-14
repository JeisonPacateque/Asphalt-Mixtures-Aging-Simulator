# -*- coding: utf-8 -*-
"""
Created on Tue Nov 25 09:31:31 2014

@author: santiago
"""

import numpy as np
import time
import math
from matplotlib import pyplot, colors


class FEMMechanics(object):
    def __init__(self, Material):
        """This class supports the Mechanic FEM Simulation"""
        self.material = Material  # Imported sample
        self.E2 = 21000000  # Agregado
        self.E1 = 10000000  # Masctic
        self.E0 = 100  # Aire
        self.L = 1.  # Longitud del elemento finito
        self.A = 1.  # Area transversal del elemento finito
        self.ki = np.zeros((1))  # Inicializa el arreglo vacio
        self.K = np.zeros((1))

        self.runSimulation()  # Ejecuta la simulacion

    def LinearBarElementForces(self, k, u):
        """This function returns the element nodalforce vector given the element 
        stiffness matrix k and the element nodal displacement vector u."""
        return np.dot(k, u)

    def LinearBarElementStresses(self, k, u, A):
        """This function returns the element nodal stress vector given the element
         stiffness matrix k, the element nodal displacement vector u, and the 
         cross-sectional area A."""
        y = np.dot(k, u)
        return y / A

    def runSimulation(self):
        print "Running mechanic simulation..."
        start_time = time.time()  # Measures Stiffness Assemble matrix time

        # Carga del Slice-----------------------------------------------
        sample = self.material.loadVerticalSlice()
        slice_size = sample.shape

        #Obtencion de los nodos superiores e inferiores--------------------
        top_nodes = self.material.conectivity.getTopElementNodes()
        bottom_nodes = self.material.conectivity.getBottomElementNodes()

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
        np.set_printoptions(threshold=np.inf, linewidth=np.inf)  # turn off summarization, line-wrapping
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
        print "Displacements done and saved in", str(end_time - start_time), "seconds."

        print "Top nodes:", len(top_nodes)
        print "Bottom nodes:", len(bottom_nodes)