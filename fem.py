# -*- coding: utf-8 -*-
"""
Created on Fri Aug  1 14:37:30 2014

@author: santiago
"""

from tvtk.api import write_data, tvtk
from sfepy.mesh.mesh_generators import gen_block_mesh
import numpy as np
import time

    
class VectorWriter(object):
    
    def __init__(self):
        pass
    
#    def toymodel_to_vector(self, collection):
#        """This method transform a segmented Toy Model object (collection) and returns
#        the model equivalent Mesh"""
#
#        size=collection.shape
#        mesh = tvtk.ImageData(spacing=(size), origin=(0, 0, 0))
#        mesh.point_data.scalars = collection.ravel(order='F')
#        mesh.point_data.scalars.name = 'scalars'
#        mesh.dimensions = collection.shape    
#        
#        return mesh
        
    def save_vtk(self, collection, filename):
        """This method saves a vectorrized Toy Model object to a VTK manipulable file"""
        
        start_time = time.time()  # Measures file loading time
        dimensions = collection.shape
        mesh = gen_block_mesh((1, 1, 1), dimensions, (0, 0, 0), name='ToyModel', verbose=True)
        mesh.mat_ids
        mesh.write(filename)
        end_time = time.time()  # Get the time when method ends
        
        print "Done writting VTK file at", filename, str(end_time - start_time), " seconds."
        
    def create_test_slice(self, toymodel):
        """Test method to perform a FEM mechanical simulation """
        print "Creating one slice"
        test_slice = toymodel[:,50,:] #Vertical slice
        #size = test_slice.shape
        polys = np.array([[0,1,3], [0,3,2], [1,2,3], [0,2,1]])
        test_mesh = tvtk.PolyData(points=test_slice, polys=polys)
        test_mesh.point_data.scalars = test_slice
        test_mesh.point_data.scalars.name = 'Temperature'
        write_data(test_mesh, '/home/santiago/tajada.vtk')
        print "Done creating one slice"