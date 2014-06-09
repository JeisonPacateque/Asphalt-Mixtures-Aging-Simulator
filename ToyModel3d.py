# -*- coding: utf-8 -*-
"""
Created on Tue May 27 09:10:49 2014

@author: sjdps
"""

from mayavi import mlab
#from tvtk.api import tvtk


def ToyModel3d(sample):
    src = mlab.pipeline.scalar_field(sample)
    
    mlab.pipeline.iso_surface(src, contours=[1], opacity=0.4)
    mlab.pipeline.image_plane_widget(src, plane_orientation='y_axes', slice_index=10)
    mlab.pipeline.scalar_cut_plane(src)
    mlab.orientation_axes()
    mlab.show()