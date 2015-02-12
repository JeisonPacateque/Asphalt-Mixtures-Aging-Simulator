# -*- coding: utf-8 -*-
"""
Created on Tue May 27 09:10:49 2014

@author: sjdps
"""

from mayavi import mlab
from numpy import array

def ToyModel3d(sample):
    """
    This script configure the 3D render motor (Mayavi) to show an interactive
    reconstruction of the asphalt mixture sample
    """
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

    #Set the Mayavi Colorbar Ranges
    scp.module_manager.scalar_lut_manager.use_default_range = False
    scp.module_manager.scalar_lut_manager.scalar_bar.position2 = array([ 0.1,  0.8])
    scp.module_manager.scalar_lut_manager.scalar_bar.position = array([ 0.01,  0.15])
    scp.module_manager.scalar_lut_manager.data_range = array([ 0.,  2.])
    scp.module_manager.scalar_lut_manager.scalar_bar.position2 = array([ 0.1,  0.8])
    scp.module_manager.scalar_lut_manager.scalar_bar.position = array([ 0.01,  0.15])
    scp.module_manager.scalar_lut_manager.data_range = array([ 0.,  2.])


    mlab.orientation_axes()
    mlab.title("Asphalt Mixture Reconstruction", size=0.25)
    mlab.colorbar(title='Material', orientation='vertical', nb_labels=3, nb_colors=3)
    mlab.show()