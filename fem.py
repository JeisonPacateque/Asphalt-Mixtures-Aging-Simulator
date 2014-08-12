# -*- coding: utf-8 -*-
"""
Created on Fri Aug  1 14:37:30 2014

@author: santiago
"""

from tvtk.api import write_data, tvtk
import numpy as np
import time

class VectorWriter(object):
    
    def __init__(self):
        pass
    
    def toymodel_to_vtk(self, toymodel, filename):
        """This method transform a segmented Toy Model object (collection) into a
        VTK manipulable file"""

        start_time = time.time()  # Measures file execution time
        
        collection = np.array(toymodel) 
        size=collection.shape
        vector_file = tvtk.ImageData(spacing=(size), origin=(0, 0, 0))
        vector_file.point_data.scalars = collection.ravel(order='F')
        vector_file.point_data.scalars.name = 'scalars'
        vector_file.dimensions = collection.shape
        
        write_data(vector_file, filename)
        print filename

        end_time = time.time()  # Get the time when method ends
        
        print "Done writting VTK file at", filename, str(end_time - start_time), " seconds."