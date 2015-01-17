# -*- coding: utf-8 -*-
"""
Created on Tue Dec  9 13:25:11 2014

@author: santiago
"""
import numpy as np
import time
from Conectivity import ConectivityMatrix

class Material(object):

    def __init__(self, collection):
        """This class handle the material to be simulated by FEM"""
        self.collection = collection  # Imported sample
        self.vertical_slice = self.loadVerticalSlice()
        self.E2 = 21000000 #Aggregate Young's modulus
        self.E1 = 10000000 #Masctic Young's modulus
        self.E0 = 100      #Air Young's modulus
        self.conductAsphalt = 0.75  #Thermal conductivity units are W/(m K) in the SI 
        self.conductAir = 0.026 #Thermal conductivity units are W/(m K) in the SI 
        self.conductRock = 7.8 #Thermal conductivity units are W/(m K) in the SI 
        self.L = 1. #Finite Element length
        self.A = 1. #Finite Element transversal area
        self.ki = np.zeros((1)) #Discrete Stiffness Matrix
        self.K = np.zeros((1)) #General Stifness Matrix
        self.conectivity = ConectivityMatrix() #General conectivity matrix
        self.thermicalConstantsMatrix = self.assignThermicalProperties(self.vertical_slice)
        self.assignMechanicalProperties(self.vertical_slice)
        self.generalStiffnessMatrixAssemble(self.vertical_slice.shape)


        
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
   
    def loadVerticalSlice(self):
        """Cut the central slice of the sample for FEM mechanics simulation"""
        vertical = self.collection[:, :, 50]
        return vertical
        
    def assignMechanicalProperties(self, sample):
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
        
    def assignThermicalProperties(self, sample):
        """Assign the material thermical constants for each pixel detected"""
        start_time = time.time()  # Measures Stiffness Assemble matrix time
        thermicalConstantsMatrix = np.zeros(sample.shape)
        for (x,y), value in np.ndenumerate(sample):
            if sample[x, y] == 2:
                thermicalConstantsMatrix[x, y] = self.conductRock
            elif sample[x, y] == 1: 
                thermicalConstantsMatrix[x, y] = self.conductAsphalt
            else:
                thermicalConstantsMatrix[x, y] = self.conductAir
        
        end_time = time.time()  # Get the time when method ends
        print "Thermal constants assignements done in", str(end_time - start_time), "seconds."
        return thermicalConstantsMatrix
        
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
        return self.K
    