# -*- coding: utf-8 -*-
"""
Created on Mon Dec  1 14:01:28 2014

@author: santiago
"""
import time

class ConectivityMatrix(object):
        def __init__(self):
            """Class intended to create the conectivity matrix for all LinearBar element nodes"""
            self.elements_nodes = []  # Tupla de nodos de cada elemento
            self.elements_top = [] # Indice Elemento superior
            self.elements_bottom = [] #Indice Elemento inferior
                
        def ElementConectivityMatrix(self, width, height):
            """Create the nodes and set positions for all elements on a stiffness matrix"""
            start_time = time.time()  # Measures file loading time
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
            end_time = time.time()  # Get the time when method ends
            print "Conectivity matrix done in", str(end_time - start_time), "seconds."
            return self.elements_nodes
            
        def getTopElementNodes(self):
            return self.elements_top
        
        def getBottomElementNodes(self):
            return self.elements_bottom