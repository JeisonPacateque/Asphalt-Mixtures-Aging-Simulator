'''
Copyright (C) 2015 Jeison Pacateque, Santiago Puerto

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
'''

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