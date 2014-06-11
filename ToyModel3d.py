# -*- coding: utf-8 -*-
"""
Created on Tue May 27 09:10:49 2014

@author: sjdps
"""

from mayavi import mlab


def ToyModel3d(sample):
    src = mlab.pipeline.scalar_field(sample)  
    inverse_lut = False
    colors = 5
    
    iso = mlab.pipeline.iso_surface(src, contours=[1], opacity=0.4, colormap = 'blue-red')
    iso.module_manager.scalar_lut_manager.reverse_lut = inverse_lut
    iso.module_manager.scalar_lut_manager.number_of_colors = colors
    
    ipw = mlab.pipeline.image_plane_widget(src, plane_orientation='y_axes', slice_index=10, colormap = 'blue-red')
    ipw.module_manager.scalar_lut_manager.reverse_lut = inverse_lut
    ipw.module_manager.scalar_lut_manager.number_of_colors = colors
    
    scp = mlab.pipeline.scalar_cut_plane(src, colormap = 'blue-red')
    scp.module_manager.scalar_lut_manager.reverse_lut = inverse_lut
    scp.module_manager.scalar_lut_manager.number_of_colors = colors
    
    mlab.orientation_axes()
    mlab.show()