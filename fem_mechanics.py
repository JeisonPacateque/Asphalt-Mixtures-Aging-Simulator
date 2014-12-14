# -*- coding: utf-8 -*-
"""
Created on Tue Nov 25 09:31:31 2014

@author: santiago
"""

import numpy as np
import time
from Conectivity import ConectivityMatrix

class FEMMechanics(object):
    
    def __init__(self, collection):
        """This class supports the Mechanic FEM Simulation"""
        self.collection = collection  # Imported sample
        self.E2 = 21000000 #Agregado
        self.E1 = 10000000 #Masctic
        self.E0 = 100      #Aire
        self.L = 1. #Longitud del elemento finito
        self.A = 1. #Area transversal del elemento finito
        self.ki = np.zeros((1)) #Inicializa el arreglo vacio
        self.K = np.zeros((1))
        self.conectivity = ConectivityMatrix()
        
        self.runSimulation() #Ejecuta la simulacion
       
    def LinearBarElementForces(self, k, u):
        """This function returns the element nodalforce vector given the element 
        stiffness matrix k and the element nodal displacement vector u."""
        return np.dot(k, u)
        
    def LinearBarElementStresses(self, k, u, A):
         """This function returns the element nodal stress vector given the element 
         stiffness matrix k, the element nodal displacement vector u, and the 
         cross-sectional area A."""
         y = np.dot(k, u)
         return y/A
        
    def runSimulation(self):
        print "Running mechanic simulation..."   
        start_time = time.time()  # Measures Stiffness Assemble matrix time
        
        #Carga del Slice-----------------------------------------------
        sample = self.loadVerticalSlice()
        slice_size = sample.shape
                
        self.assignMaterialProperties(sample)
        self.generalStiffnessMatrixAssemble(slice_size)
       
        
        #Obtencion de los nodos superiores e inferiores--------------------
        top_nodes = self.conectivity.getTopElementNodes()
        bottom_nodes = self.conectivity.getBottomElementNodes()
        
        mask = np.ones(self.K.shape[0], dtype=bool)
        mask[bottom_nodes] = False
        k_sub = self.K[mask]
        k_sub = k_sub[:, mask]
        
        #Aplicar fuerzas sobre el modelo------------------------------------
        force = 200
        Fuerzas = force*np.ones(k_sub.shape[0])
        
        #Calcular desplazamientos-------------------------------------------
        U = np.linalg.solve(k_sub, Fuerzas)
        
        end_time = time.time()  # Get the time when method ends
        print "Displacements done in", str(end_time - start_time), "seconds."        
                
        print "Top nodes:", len(top_nodes)
        print "Bottom nodes:", len(bottom_nodes)