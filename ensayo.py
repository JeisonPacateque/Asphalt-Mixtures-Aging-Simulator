# -*- coding: utf-8 -*-
"""
Created on Tue Nov 25 09:31:31 2014

@author: santiago
"""

import numpy as np
from Conectivity import ConectivityMatrix

def LinearBarElementStiffness(E, A, L):
    return np.array([[E*(A/L), -E*(A/L)], [-E*(A/L) ,E*(A/L)]])
    
def LinearBarAssemble(K, k, i, j):
    K[i][i] = K [i][i] + k[0][0]
    K[i][j] = K [i][j] + k[0][1]
    K[j][i] = K [j][i] + k[1][0]
    K[j][j] = K [j][j] + k[1][1]    
    return K
    
def LinearBarElementForces(k, u):
    return np.dot(k, u)
    
def LinearBarElementStresses(k, u, A):
    y = np.dot(k, u)
    return y/A

#def ElementConectivityMatrix(width, height):
#    elements = []
#    a = 0
#    b = 1
#    for i in range(width):
#        print "Primero"
#        for j in range(height):
#            elements.append((a, b))
#            a=a+1
#            b=b+1
##        print "Ultimo"      
#        a=a+1
#        b=b+1
#    return elements

def loadSample():
    import file_loader
    import segmentation
    
    Loader = file_loader.FileLoader()
    Seg = segmentation.Segmentation()
    
    path = "/home/santiago/Proyecto-de-Grado-Codes/samples/4"
    collection = Loader.load_path(path) #Load Files
    print str(len(collection))+" DICOM files loaded."
        
    scaled = Seg.reduction(collection)
    toymodel = Seg.segment_all_samples(scaled)
    
    tajada = toymodel[:, :, 50]
    return tajada
    
E2 = 21000000 #Agregado
E1 = 10000000 #Masctic
E0 = 100      #Aire
L = 1.
A = 1.

tajada = loadSample()
tam = tajada.shape
conectivity = ConectivityMatrix()
con_mtrx = conectivity.ElementConectivityMatrix(tam[0], tam[1])

#archivo = open("matrix_conectivity", 'w')
#archivo.write(str(conectivity))
#archivo.close()


#ki = []
#
#for i in range(tam[0]):
#    for j in range(tam[1]):
#        if tajada[i][j]==2:
#            ki.append(LinearBarElementStiffness(E2, A, L))
#        elif tajada[i][j]==1:
#            ki.append(LinearBarElementStiffness(E1, A, L))
#        else:
#            ki.append(LinearBarElementStiffness(E0, A, L))

ki = np.empty(tajada.size, dtype=object)
print "tajada shape", tajada.shape

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

K = np.zeros((4600, 4600))

#print "tamaño ki", len(ki)
#print "tamaño conec", len(conectivity)
#print conectivity[-1]


cont = 0
for y in con_mtrx: #Ensamble de la matriz de rigidez general
    K = LinearBarAssemble(K, ki[cont], y[0], y[1])
    cont = cont+1
 
print "K shape", K.shape


top_nodes = conectivity.getTopElementNodes()
bottom_nodes = conectivity.getBottomElementNodes()


mask = np.ones(K.shape[0], dtype=bool)
mask[bottom_nodes] = False
k_sub = K[mask]
k_sub = k_sub[:, mask]

force = 20
Fuerzas = force*np.ones(k_sub.shape[0])

U = np.linalg.solve(k_sub, Fuerzas)


#print "top", top_nodes
#print "bottom", bottom_nodes

print "top len", len(top_nodes)
print "bottom len", len(bottom_nodes)


#print "prueba shape", prueba.shape

#print np.allclose(K, np.diag(np.diag(K)))
#archivo = open("matrix_K", 'w')
#archivo.write(str(K))
#archivo.close()
