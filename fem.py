# -*- coding: utf-8 -*-
"""
Created on Fri Aug  1 14:37:30 2014

@author: santiago
"""

import sfepy.mesh.mesh_generators as generator
import numpy as np
import time

    
class VectorWriter(object):
    
    def __init__(self):
        pass
    
#    def save_vtk(self, collection, filename):
#        """This method saves the Toy Model object to a VTK manipulable file"""
#        
#        start_time = time.time()  # Measures file loading time
#        
#        dims = collection.shape
#        x_lenght = dims[1]/2
#        y_lenght = dims[2]/2
#        z_lenght = dims[0]
#        
#        dimensiones = (0, 0, x_lenght, y_lenght, dims[0])
#        forma = (x_lenght, y_lenght, dims[0])
#        centro = (x_lenght/2, y_lenght/2, z_lenght/2)
#        
#        mesh = generator.gen_cylinder_mesh(dimensiones, forma, centro, axis='z', force_hollow=False, non_uniform=False ,name='ToyModel', verbose=True )
#        
#        mesh.write(filename)
#        end_time = time.time()  # Get the time when method ends
#        
#        print "Done writting VTK file at", filename, str(end_time - start_time), " seconds."
       
         
    def save_vtk(self, collection, filename):
        """This method saves the Toy Model object to a VTK manipulable file"""
        
        start_time = time.time()  # Measures file loading time
        
        #dimensions = collection.shape
        dimensions = np.array((23, 99, 100))
        #print dimensions
    
        mesh = generator.gen_block_mesh(dimensions, dimensions, (0, 0, 0), name='ToyModel', verbose=True)
        
        mesh.write(filename)
        end_time = time.time()  # Get the time when method ends
        
        print "Done writting VTK file at", filename, str(end_time - start_time), " seconds."
       