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
    
    def LinearBarElementStiffness(self, E, A, L):
        """ This function returns the element stiffness matrix for a linear bar with
        modulus of elasticity E, cross-sectional area A, and length L. The size of 
        the element stiffness matrix is 2 x 2."""
        return np.array([[E*(A/L), -E*(A/L)], [-E*(A/L) ,E*(A/L)]])
    
    def LinearBarAssemble(self, K, k, i, j):
        """This function assembles the element stiffness matrix k of the linear bar 
        with nodes i and j into the global stiffness matrix K.This function returns 
        the global stiffness matrix K after the element stiffness matrix k is assembled."""
        K[i][i] = K [i][i] + k[0][0]
        K[i][j] = K [i][j] + k[0][1]
        K[j][i] = K [j][i] + k[1][0]
        K[j][j] = K [j][j] + k[1][1]    
        return K
    
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

    def loadVerticalSlice(self):
        """Cut the central slice of the sample for FEM mechanics simulation"""
        segmented = self.collection
        vertical_slice = segmented[:, :, 50]
        return vertical_slice
        
    def assignMaterialProperties(self, sample):
        """Load the sample and assing the material modulus for each pixel detected"""
        start_time = time.time()  # Measures Stiffness Assemble matrix time
        self.ki = np.empty(sample.size, dtype=object)#Creacion de la matriz de rigidez vacia
#        print "Loaded slice shape:", sample.shape
        cont=0
        
        for x in np.nditer(sample):
        #    print x
            if x==2:
                self.ki[cont] = self.LinearBarElementStiffness(self.E2, self.A, self.L)
            elif x==1:
                self.ki[cont] = self.LinearBarElementStiffness(self.E1, self.A, self.L)
            else:
                self.ki[cont] = self.LinearBarElementStiffness(self.E0, self.A, self.L)
            
            cont=cont+1
            
        end_time = time.time()  # Get the time when method ends
        print "Material assignements done in", str(end_time - start_time), "seconds."
        
    def generalStiffnessMatrixAssemble(self, slice_size):
        """Assembles an n x n Stiffness Matrix"""
        start_time = time.time()  # Measures Stiffness Assemble matrix time
        #Creacion de la matriz de conectividad------------------------
        
        con_mtrx = self.conectivity.ElementConectivityMatrix(slice_size[0], slice_size[1])
        self.K = np.zeros((4600, 4600))
        
        cont = 0
        for y in con_mtrx: 
            self.K = self.LinearBarAssemble(self.K, self.ki[cont], y[0], y[1])
            cont = cont+1
         
#        print "General Stiffness Matriz shape:", self.K.shape
        
        end_time = time.time()  # Get the time when method ends
        print "General Stiffness Matriz done in", str(end_time - start_time), "seconds."        
        
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