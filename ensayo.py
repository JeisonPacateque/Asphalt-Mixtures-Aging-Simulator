# -*- coding: utf-8 -*-
"""
Created on Tue Nov 25 09:31:31 2014

@author: santiago
"""

import numpy as np
from Conectivity import ConectivityMatrix

def LinearBarElementStiffness(E, A, L):
    """ This function returns the element stiffness matrix for a linear bar with
    modulus of elasticity E, cross-sectional area A, and length L. The size of 
    the element stiffness matrix is 2 x 2."""
    return np.array([[E*(A/L), -E*(A/L)], [-E*(A/L) ,E*(A/L)]])
    
def LinearBarAssemble(K, k, i, j):
    """This function assembles the element stiffness matrix k of the linear bar 
    with nodes i and j into the global stiffness matrix K.This function returns 
    the global stiffness matrix K after the element stiffness matrix k is assembled."""
    K[i][i] = K [i][i] + k[0][0]
    K[i][j] = K [i][j] + k[0][1]
    K[j][i] = K [j][i] + k[1][0]
    K[j][j] = K [j][j] + k[1][1]    
    return K
    
def LinearBarElementForces(k, u):
    """This function returns the element nodalforce vector given the element 
    stiffness matrix k and the element nodal displacement vector u."""
    return np.dot(k, u)
    
def LinearBarElementStresses(k, u, A):
     """This function returns the element nodal stress vector given the element 
     stiffness matrix k, the element nodal displacement vector u, and the 
     cross-sectional area A."""
     y = np.dot(k, u)
     return y/A

def loadSample():
    import file_loader
    import segmentation
    
    Loader = file_loader.FileLoader()
    Seg = segmentation.Segmentation()
    
    path = "samples/4"
    collection = Loader.load_path(path) #Load Files
    print str(len(collection))+" DICOM files loaded."
        
    scaled = Seg.reduction(collection)
    toymodel = Seg.segment_all_samples(scaled)
    
    tajada = toymodel[:, :, 50]
    return tajada
    
#Definiciones del problema-----------------------------
E2 = 21000000 #Agregado
E1 = 10000000 #Masctic
E0 = 100      #Aire
L = 1. #Longitud del elemento finito
A = 1. #Area transversal del elemento finito


#Carga del Slice-----------------------------------------------
tajada = loadSample()
tam = tajada.shape

#Creacion de la matriz de conectividad------------------------
conectivity = ConectivityMatrix()
con_mtrx = conectivity.ElementConectivityMatrix(tam[0], tam[1])


#archivo = open("matrix_conectivity", 'w')
#archivo.write(str(conectivity))
#archivo.close()

#Creacion de la matriz de rigidez vacia--------------------------
ki = np.empty(tajada.size, dtype=object)
print "Loaded slice shape", tajada.shape


#Asignacion de modulo segun material en la muestra----------------
import time
start_time = time.time()  # Measures Stiffness Assemble matrix time

cont=0
for x in np.nditer(tajada):
#    print x
    if x==2:
        ki[cont] = LinearBarElementStiffness(E2, A, L)
    elif x==1:
        ki[cont] = LinearBarElementStiffness(E1, A, L)
    else:
        ki[cont] = LinearBarElementStiffness(E0, A, L)
    
    cont=cont+1

#Ensamble de la matriz de rigidez general----------------------------
K = np.zeros((4600, 4600))
cont = 0

for y in con_mtrx: 
    K = LinearBarAssemble(K, ki[cont], y[0], y[1])
    cont = cont+1
 
print "K shape", K.shape

#Obtencion de los nodos superiores e inferiores--------------------

top_nodes = conectivity.getTopElementNodes()
bottom_nodes = conectivity.getBottomElementNodes()

mask = np.ones(K.shape[0], dtype=bool)
mask[bottom_nodes] = False
k_sub = K[mask]
k_sub = k_sub[:, mask]

#Aplicar fuerzas sobre el modelos-----------------------------------
force = 20
Fuerzas = force*np.ones(k_sub.shape[0])

#Calcular desplazamientos-------------------------------------------
U = np.linalg.solve(k_sub, Fuerzas)

end_time = time.time()  # Get the time when method ends
print "Displacements done in: ", str(end_time - start_time), " seconds."

#print "top", top_nodes
#print "bottom", bottom_nodes

print "top len", len(top_nodes)
print "bottom len", len(bottom_nodes)
